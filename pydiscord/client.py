import aiohttp
import asyncio
import json
import time
import logging
from typing import Callable
from .user import User
from .guild import Guild, GuildMember
from .base import DiscordObject

FORMAT = '%(asctime)-15s: %(message)s'
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('DiscordClient')


class RateLimit(DiscordObject):
    def __init__(self, message="", retry_after=0, _global=False):
        self.message = message
        self.retry_after = retry_after
        self._global = _global


class HTTPHandler:
    def __init__(self, token):
        self.token = token
        self.loop = asyncio.get_event_loop()
        self.headers = ''
        self.discord_url = 'https://discordapp.com/api'
        self.update_headers()

    def update_headers(self):
        self.headers = {'Authorization': 'Bot ' + self.token}

    async def request_url(self, url):
        while True:
            async with aiohttp.ClientSession(headers=self.headers) as session:
                async with session.get(self.discord_url + url) as res:
                    logger.debug(await res.text())
                    logger.debug(res.status)
                    if res.status == 429:
                        text = await res.text()
                        limit = RateLimit.from_json(text)
                        # TODO: Handle global rate limit?

                        if 'X-RateLimit-Remaining' in res.headers and int(res.headers['X-RateLimit-Remaining']) > 0:
                            logger.debug(f"Status is {res.status} but i have {res.headers['X-RateLimit-Remaining']} ratelimits remaining, ")
                            continue

                        logger.debug(
                            f"Status is {res.status} so we must wait {limit.retry_after / 1000} seconds!")
                        await asyncio.sleep(limit.retry_after / 1000)
                        logger.debug("Done waiting! Requesting again")
                    elif res.status == 200:
                        return res
                    elif res.status == 401:
                        text = await res.text()
                        logger.warning(f"You requested a api endpoint which you have no authorization: {text}")
                        return res 
                    else:
                        logger.warning(
                            f"Unhandled response status when requesting url = '{url}'")
                        return res


class DiscordBot:
    def __init__(self, token):
        """DiscordBot constructor.

        Args:
            token (str): The bot discord token.
        """
        self.token = token
        self.httpHandler = HTTPHandler(token)
        loop = asyncio.get_event_loop()
        self.user = loop.run_until_complete(self.get_self_user())

    def run(self):
        loop = asyncio.get_event_loop()

    async def event(self, func):
        if func.__name__ == 'on_message':
            pass
        pass

    async def change_avatar(self, url):
        pass  # TODO: Implement this: https://discordapp.com/developers/docs/resources/user#modify-current-user

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
            logger.debug(text)
            guild._fill_members(text)
            return True
        else:
            return False

    async def get_guild_member(self, guild: Guild, id):
        res = await self.httpHandler.request_url('/guilds/' + guild.id + '/members/' + id)
        if res.status == 200:
            text = await res.text()
            logger.debug(text)
            return GuildMember.from_json(text)
        else:
            return None

    async def get_dms(self):
        pass  # TODO: Implement this: https://discordapp.com/developers/docs/resources/user#modify-current-user
