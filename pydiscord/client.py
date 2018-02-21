import aiohttp
import asyncio
import json
import time
import logging
from .user import User
from .guild import Guild, GuildMember
from .base import DiscordObject
from .version import VERSION_STR
from .constants import DISCORD_API_URL
from .channel import Channel

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
        self.update_headers()
        self.session = None

    async def create_session(self):
        self.session = aiohttp.ClientSession(headers=self.headers)

    def update_headers(self):
        self.headers = {'Authorization': 'Bot ' + self.token,
                        'User-Agent': f'DiscordBot (https://github.com/Ryozuki/pydiscord, {VERSION_STR})'}

    async def request_url(self, url, type='GET', data=None):
        while True:
            operation = None
            if type == 'GET':
                operation = self.session.get(DISCORD_API_URL + url)
            elif type == 'POST':
                operation = self.session.post(DISCORD_API_URL + url, data)
            elif type == 'DELETE':
                operation = self.session.delete(DISCORD_API_URL + url)

            async with operation as res:
                # logger.debug(await res.text())
                # logger.debug(res.status)
                if res.status == 429:
                    text = await res.text()
                    limit = RateLimit.from_json(text)
                    # TODO: Handle global rate limit?

                    if 'X-RateLimit-Remaining' in res.headers and int(res.headers['X-RateLimit-Remaining']) > 0:
                        logger.debug(
                            f"Status is {res.status} but i have {res.headers['X-RateLimit-Remaining']} ratelimits remaining, ")
                        continue

                    logger.debug(
                        f"Status is {res.status} so we must wait {limit.retry_after / 1000} seconds!")
                    await asyncio.sleep(limit.retry_after / 1000)
                    logger.debug("Done waiting! Requesting again")
                elif res.status == 200:
                    return res
                elif res.status == 204 and type == 'DELETE':
                    return res
                elif res.status == 401:
                    logger.warning(
                        f"You requested a api endpoint which you have no authorization: {text}")
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
    
    async def start(self):
        await self.httpHandler.create_session()
        self.user = await self.get_self_user()

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
        pass  # TODO: Implement this: https://discordapp.com/developers/docs/resources/user#modify-current-user
