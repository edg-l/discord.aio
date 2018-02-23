import aiohttp
import asyncio
import json
import time
import logging
import signal
from concurrent.futures import ProcessPoolExecutor
from threading import Thread

from .exceptions import EventTypeException
from .user import User, UserConnection
from .guild import Guild, GuildMember
from .base import DiscordObject
from .version import PYDISCORD_VERSION_STR
from .constants import DISCORD_API_URL
from .channel import Channel
from .http import HTTPHandler

logger = logging.getLogger('DiscordClient')


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
                raise EventTypeException(
                    'The event function must be a coroutine.')
            if name is not None:
                if not isinstance(name, str):
                    raise TypeError('event name must be of type str')
                else:
                    try:
                        getattr(self, name)
                        raise AttributeError(
                            'tried to subscribe to a event that doesn\'t exist')
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
        if res.status == 200:
            text = await res.text()
            return User.from_json(text)
        else:
            return None

    async def get_self_user(self):
        """Requests information about the current user."""

        return await self.get_user("@me")

    async def get_guilds(self):
        """Returns the list of guilds that the user belongs to.

        Returns:
            [Guild]: The array of guilds.
        """
        res = await self.httpHandler.request_url('/users/@me/guilds')
        if res.status == 200:
            text = await res.text()
            return Guild.from_json_array(text)
        else:
            return None

    async def get_guild(self, id):
        res = await self.httpHandler.request_url('/guilds/' + str(id))
        if res.status == 200:
            text = await res.text()
            return Guild.from_json(text)
        else:
            return None

    async def get_guild_members(self, guild: Guild):
        """Gets and fills the guild with it's members info

        Returns:
            bool: True if succeeds, False if not."""
        res = await self.httpHandler.request_url('/guilds/' + guild.id + '/members')
        if res.status == 200:
            text = await res.text()
            guild._fill_members(text)
            return True
        else:
            return False

    async def get_guild_member(self, guild: Guild, member_id):
        res = await self.httpHandler.request_url('/guilds/' + guild.id + '/members/' + member_id)
        if res.status == 200:
            text = await res.text()
            return GuildMember.from_json(text)
        else:
            return None

    async def leave_guild(self, guild_id):
        res = await self.httpHandler.request_url(f'/users/@me/guilds/{guild_id}', type='DELETE')
        if res.status == 204:
            return True
        else:
            return False

    async def get_channel(self, channel_id):
        res = await self.httpHandler.request_url(f'/channels/{channel_id}')
        if res.status == 200:
            text = await res.text()
            return Channel.from_json(text)
        else:
            return None

    async def delete_channel(self, channel_id):
        res = await self.httpHandler.request_url(f'/channels/{channel_id}', type='DELETE')
        if res.status == 204:
            return True
        else:
            return False

    async def get_dms(self):
        res = await self.httpHandler.request_url('/users/@me/channels')
        if res.status == 200:
            text = await res.json()
            return list(Channel.from_dict_array(text))
        else:
            return None

    async def get_connections(self):
        res = await self.httpHandler.request_url('/users/@me/connections')
        if res.status == 200:
            text = await res.json()
            logger.debug(text)
            return list(UserConnection.from_dict_array(text))
        else:
            return None
