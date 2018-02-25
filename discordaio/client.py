import aiohttp
import asyncio
import json
import time
import signal
from typing import Optional, List

from .exceptions import EventTypeError
from .user import User, UserConnection
from .guild import Guild, GuildMember
from .base import DiscordObject
from .constants import DISCORD_API_URL
from .channel import Channel
from .http import HTTPHandler
from .websocket import DiscordWebsocket

import logging
logger = logging.getLogger(__name__)

# TODO: Delete this when sure.
# def task_handler() -> None:
#     logger.debug('Stopping tasks')
#     for task in asyncio.Task.all_tasks():
#         task.cancel()


class DiscordBot:
    """This class represents a discord bot object, it has many utility methods for making a bot.

    .. versionadded:: 0.2.0

    Attributes:
        token (:obj:`str`): The discord token used for authentication
        http (:class:`.HTTPHandler`): Used for making http requests and websocket creation.
        guilds (:obj:`list` of :class:`.Guild`): The list of guilds the bot is in.
        user (:class:`.User`): The user object of the bot.
        ws (:class:`.DiscordWebsocket`): The websocket used for communication
    """

    def __init__(self, token: str):
        """DiscordBot constructor.

        Args:
            token (obj:`str`): The discord token used for authentication.
        """
        self.token: str = token
        self.http: HTTPHandler = HTTPHandler(token, self)
        self.guilds: List[Guild] = []
        self.loop = asyncio.get_event_loop()
        self.do_sync = self.loop.run_until_complete
        self.user: Optional[User] = None
        self.ws: Optional[DiscordWebsocket] = None

    def run(self) -> None:
        """Starts the bot, making it connect to discord.

        .. versionadded:: 0.2.0
        """
        try:
            self.do_sync(self._start())
        except KeyboardInterrupt:
            pass
        except asyncio.CancelledError:
            logger.debug('Tasks has been cancelled')
        finally:
            self.do_sync(self.http.close_session())
            self.loop.close()

    async def raise_event(self, event: str, *args, **kwargs) -> None:
        try:
            if hasattr(self, event):
                await getattr(self, event)(*args, **kwargs)
        except asyncio.CancelledError as e:
            logger.error(e, exc_info=1)
            pass
        except Exception as e:
            logger.error(e, exc_info=1)
            # TODO: handle error here
            pass

    def event(self, name: str=None):
        """DiscordBot event decorator, uses the function's name or the 'name' parameter to subscribe to a event

        .. versionadded:: 0.2.0
        """
        def real_event(coro):
            if not asyncio.iscoroutinefunction(coro):
                raise EventTypeError(
                    'The event function must be a coroutine.')
            if name is not None:
                if not isinstance(name, str):
                    raise TypeError('event name must be of type str')
                else:
                    try:
                        getattr(self, name)
                        raise AttributeError(
                            'tried to subscribe to a event that doesn\'t exist, or you already subscribed to it.')
                    except AttributeError:
                        pass
                    finally:
                        setattr(self, name, coro)
            else:
                setattr(self, coro.__name__, coro)
            logger.debug(f'{coro.__name__} subscribed succesfully.')
            return coro
        return real_event

    async def _start(self):
        """Used internally by the bot to start the http session and the websocket

        .. versionadded:: 0.2.0
        """
        await self.http.create_session()
        self.ws = DiscordWebsocket(self.http)
        await self.ws.start()

    async def exit(self):
        """Disconnects the bot

        .. versionadded:: 0.2.0
        """
        if not self.ws.closed:
            await self.ws.close()
        await self.http.close_session()

    async def change_avatar(self, url: str):
        raise NotImplementedError()
        # TODO: Implement this: https://discordapp.com/developers/docs/resources/user#modify-current-user

    async def get_user(self, id: int) -> User:
        """Gets the user object from the given user id.

        .. versionadded:: 0.2.0

        Args:
            id (:obj:`int`): The user id

        Returns:
            :class:`.User`: The requested user
        """
        res = await self.http.request_url('/users/' + str(id))
        return await User.from_api_res(res)

    async def get_self_user(self) -> User:
        """Returns the bot user object. (it's like `get_user('@me')`)

        .. versionadded:: 0.2.0
        """
        return await self.get_user("@me")

    async def get_guilds(self) -> list:
        """Returns a list of guilds where the bot is in.

        .. versionadded:: 0.2.0
        """
        res = await self.http.request_url('/users/@me/guilds')
        return await Guild.from_api_res(res)

    async def get_guild(self, guild_id: int) -> Guild:
        """Returns a Guild object from a guild id.

        .. versionadded:: 0.2.0

        Args:
            guild_id (:obj:`int`): The guild id

        Returns:
            :class:`.Guild`: The requested guild
        """
        res = await self.http.request_url('/guilds/' + str(guild_id))
        return await Guild.from_api_res(res)

    async def get_guild_members(self, guild: Guild):
        """Gets and fills the guild with the members info.

        .. versionadded:: 0.2.0

        Args:
            guild (:class:`.Guild`): The guild to fill the members.
        """
        res = await self.http.request_url('/guilds/' + guild.id + '/members')
        await guild._fill_members(res)

    async def get_guild_member(self, guild: Guild, member_id: int) -> GuildMember:
        """Gets a guild member info for the guild and the member id.

        .. versionadded:: 0.2.0

        Args:
            guild (:class:`.Guild`): The guild
            member_id (:obj:`int`): The member id

        Returns:
            :class:`.GuildMember`: The guild member
        """
        res = await self.http.request_url('/guilds/' + guild.id + '/members/' + member_id)
        return await GuildMember.from_api_res(res)

    async def leave_guild(self, guild_id: int):
        """Leaves a guild.

        .. versionadded:: 0.2.0

        Args:
            guild_id (:obj:`int`): The guild id
        """
        await self.http.request_url(f'/users/@me/guilds/{guild_id}', type='DELETE')

    async def get_channel(self, channel_id: int) -> Channel:
        """Gets a channel from it's id

        .. versionadded:: 0.2.0

        Args:
            channel_id (:obj:`int`): The channel id

        Returns:
            :class:`.Channel`: The channel
        """
        res = await self.http.request_url(f'/channels/{channel_id}')
        return await Channel.from_api_res(res)

    async def delete_channel(self, channel_id: int) -> Channel:
        """Deletes a channel.

        Note:
            Delete a channel, or close a private message. Requires the 'MANAGE_CHANNELS' permission for the guild.
            Deleting a category does not delete its child channels; they will have their parent_id removed and a Channel Update Gateway event will fire for each of them.
            Returns a channel object on success.
            Fires a Channel Delete Gateway event.

        .. versionadded:: 0.2.0

        Args:
            channel_id (:obj:`int`): The channel id

        Returns:
            :class:`.Channel`: The deleted channel
        """
        res = await self.http.request_url(f'/channels/{channel_id}', type='DELETE')
        return await Channel.from_api_res(res)

    async def get_dms(self) -> list:
        """Gets a list of dms.

        .. versionadded:: 0.2.0

        Returns:
            :obj:`list` of :class:`.Channel`: The DMs channels
        """
        res = await self.http.request_url('/users/@me/channels')
        return await Channel.from_api_res(res)

    async def get_connections(self) -> list:
        res = await self.http.request_url('/users/@me/connections')
        return await UserConnection.from_api_res(res)


__all__ = [
    'DiscordBot',
]
