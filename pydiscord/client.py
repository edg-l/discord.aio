import aiohttp
import asyncio
import json
from .user import User


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
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(self.discord_url + url) as res:
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
        loop.close()

    def run(self):
        loop = asyncio.get_event_loop()
        loop.close()

    async def change_avatar(self, url):
        pass # TODO: Implement this: https://discordapp.com/developers/docs/resources/user#modify-current-user

    async def get_user(self, id):
        """Request a user information.

        Args:
            id (int): The id of the user.
        Returns:
            User: The requested user
        """

        res = await self.httpHandler.request_url('/users/' + id)
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

        pass # TODO: Implement this: https://discordapp.com/developers/docs/resources/user#get-current-user-guilds
    
    async def get_dms(self):
        pass # TODO: Implement this: https://discordapp.com/developers/docs/resources/user#modify-current-user