import aiohttp
import asyncio
import json
import time
import signal
from threading import Thread

from .exceptions import EventTypeError
from .user import User, UserConnection
from .guild import Guild, GuildMember
from .base import DiscordObject
from .version import PYDISCORD_VERSION_STR
from .constants import DISCORD_API_URL
from .channel import Channel
from .http import HTTPHandler

import logging
logger = logging.getLogger(__name__)


def task_handler():
    logger.debug('Stopping tasks')
    for task in asyncio.Task.all_tasks():
        task.cancel()


class DiscordBot:
    def __init__(self, token):
        """DiscordBot constructor.

        Args:
            token (str): The bot discord token.
        """
        self.token = token
        self.httpHandler = HTTPHandler(token, self)
        self.guilds = []
        self.loop = asyncio.get_event_loop()
        self.do_sync = self.loop.run_until_complete
        self.loop.add_signal_handler(signal.SIGINT, task_handler)

    def run(self):
        try:
            self.do_sync(self.start())
        except KeyboardInterrupt:
            # TODO: Add bot close code here
            pass
        except asyncio.CancelledError:
            logger.debug('Tasks has been cancelled')
        finally:
            self.do_sync(self.httpHandler.close_session())
            self.loop.close()

    async def raise_event(self, event, *args, **kwargs):
        try:
            await getattr(self, event)(*args, **kwargs)
        except asyncio.CancelledError:
            pass
        except Exception:
            # TODO: handle error here
            pass

    def event(self, name=None):
        """DiscordBot event decorator, uses the function's name or the 'name' parameter to subscribe to a event"""
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

    async def start(self):
        await self.httpHandler.create_session()
        await self.httpHandler.start_websocket()

    async def change_avatar(self, url):
        raise NotImplementedError()
        # TODO: Implement this: https://discordapp.com/developers/docs/resources/user#modify-current-user

    async def get_user(self, id) -> User:
        """Request a user information.

        Args:
            id (int): The id of the user.
        Returns:
            User: The requested user
        """

        res = await self.httpHandler.request_url('/users/' + str(id))
        return await User.from_api_res(res)

    async def get_self_user(self):
        """Requests information about the current user."""

        return await self.get_user("@me")

    async def get_guilds(self):
        """Returns the list of guilds that the user belongs to.

        Returns:
            [Guild]: The array of guilds.
        """
        res = await self.httpHandler.request_url('/users/@me/guilds')
        return await Guild.from_api_res(res)

    async def get_guild(self, id):
        res = await self.httpHandler.request_url('/guilds/' + str(id))
        return await Guild.from_api_res(res)

    async def get_guild_members(self, guild: Guild):
        """Gets and fills the guild with it's members info"""

        res = await self.httpHandler.request_url('/guilds/' + guild.id + '/members')
        guild._fill_members(res)

    async def get_guild_member(self, guild: Guild, member_id):
        res = await self.httpHandler.request_url('/guilds/' + guild.id + '/members/' + member_id)
        return await GuildMember.from_api_res(res)

    async def leave_guild(self, guild_id):
        res = await self.httpHandler.request_url(f'/users/@me/guilds/{guild_id}', type='DELETE')
        # TODO: redo this! it doesnt work anymore due to res not being a ClientResponse!
        if res.status == 204:
            return True
        else:
            return False

    async def get_channel(self, channel_id):
        res = await self.httpHandler.request_url(f'/channels/{channel_id}')
        return await Channel.from_api_res(res)

    async def delete_channel(self, channel_id):
        res = await self.httpHandler.request_url(f'/channels/{channel_id}', type='DELETE')
        # TODO: redo this! it doesnt work anymore due to res not being a ClientResponse!
        if res.status == 204:
            return True
        else:
            return False

    async def get_dms(self):
        res = await self.httpHandler.request_url('/users/@me/channels')
        return await Channel.from_api_res(res)

    async def get_connections(self):
        res = await self.httpHandler.request_url('/users/@me/connections')
        return await UserConnection.from_api_res(res)
