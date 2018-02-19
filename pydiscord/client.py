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
        self.token = token
        self.httpHandler = HTTPHandler(token)

    async def get_user(self, id):
        """Requests the information of a user
        """

        res = await self.httpHandler.request_url('/users/' + id)
        if res.status == 200:
            text = await res.text()
            user = json.loads(text)
            return User(user['id'], user['username'], user['discriminator'],
                        user['avatar'], user['bot'], user['mfa_enabled'],
                        user['verified'], user['email'])
        else:
            return None

    async def get_self(self):
        return await self.get_user("@me")
