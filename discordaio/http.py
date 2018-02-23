import aiohttp
import asyncio
import json
import logging
import platform

from .user import User, UserConnection
from .guild import Guild, GuildMember
from .base import DiscordObject
from .version import PYDISCORD_VERSION_STR
from .constants import DISCORD_API_URL
from .channel import Channel
from .exceptions import WebSocketCreationError, AuthorizationError, UnhandledEndpointStatusError
from .enums import GatewayOpcodes

import logging
logger = logging.getLogger(__name__)


class RateLimit(DiscordObject):
    def __init__(self, message="", retry_after=0, _global=False):
        self.message = message
        self.retry_after = retry_after
        self._global = _global


class HTTPHandler:
    def __init__(self, token, discord_client):
        self.token = token
        self.loop = asyncio.get_event_loop()
        self.headers = ''
        self.update_headers()
        self.session = None
        self.discord_client = discord_client

    async def create_session(self):
        self.session = aiohttp.ClientSession(
            headers=self.headers, auto_decompress=True)

    async def close_session(self):
        await self.session.close()

    async def start_websocket_in_thread(self):
        #self.loop = asyncio.new_event_loop()
        await self.start_websocket()
        # self.loop.close()

    async def start_websocket(self):
        info = await self.request_url('/gateway/bot')
        self.gateway_url = info['url']
        self.shards = info['shards']
        logger.debug(f'I can use {self.shards} shards!')
        self.heartbeat_interval = None
        self._trace = None
        self.s = None
        self.heartbeat_future = None
        self.session_id = None
        async with self.session.ws_connect(self.gateway_url + '?v=6&encoding=json') as ws:
            async for msg in ws:
                # logger.debug(msg)
                if msg.type == aiohttp.WSMsgType.TEXT:
                    dct = json.loads(msg.data)
                    opcode = dct['op']
                    data = dct['d']
                    if GatewayOpcodes(opcode) == GatewayOpcodes.HELLO:
                        if self.heartbeat_future is not None:
                            if not self.heartbeat_future.cancelled():
                                self.heartbeat_future.cancel()
                                self.heartbeat_future = None
                        self.heartbeat_interval = dct['d']['heartbeat_interval']
                        self._trace = dct['d']['_trace']
                        self.s = dct['s']
                        await ws.send_json({
                            "op": 2,  # Identify
                            "d": {
                                "token": self.token,
                                "properties": {
                                    '$os': platform.system(),
                                    '$browser': 'PyDiscord',
                                    '$device': 'PyDiscord'
                                },
                                "compress": False,
                                "large_threshold": 250
                            }
                        })
                        logger.debug(
                            f'Ensuring to heartbeat every {self.heartbeat_interval / 1000} seconds!')
                        self.heartbeat_future = asyncio.ensure_future(
                            self.send_heartbeat(ws))
                    elif GatewayOpcodes(opcode) == GatewayOpcodes.HEARTBEAT_ACK:
                        logger.debug(
                            f'Got HEARTBEAT_ACK (new s: {dct["s"]}, old s: {self.s})')
                        self.s = dct['s']
                    elif GatewayOpcodes(opcode) == GatewayOpcodes.DISPATCH:
                        event_type = dct['t']
                        if event_type == 'READY':
                            self.session_id = data['session_id']
                            self.discord_client.user = await User.from_api_res(data['user'])
                            self.discord_client.guilds = await Guild.from_api_res(data['guilds'])
                            asyncio.ensure_future(
                                self.discord_client.raise_event('on_ready', dct['d']))

    async def send_heartbeat(self, ws):
        while True:
            logger.debug(
                f'Waiting {self.heartbeat_interval / 1000} seconds to send heartbeat')
            await asyncio.sleep(self.heartbeat_interval / 1000)
            await ws.send_json({
                'op': 1,
                'd': self.s
            })
            logger.debug("Sent heartbeat")

    def update_headers(self):
        self.headers = {'Authorization': 'Bot ' + self.token,
                        'User-Agent': f'DiscordBot (https://github.com/Ryozuki/pydiscord, {PYDISCORD_VERSION_STR})'}

    async def request_url(self, url, type='GET', data=None):
        while True:
            # TODO: Handle aiohttp.client_exceptions.ClientConnectionError: Connection closed
            operation = None
            if type == 'GET':
                operation = self.session.get(DISCORD_API_URL + url)
            elif type == 'POST':
                operation = self.session.post(DISCORD_API_URL + url, data=data)
            elif type == 'DELETE':
                operation = self.session.delete(DISCORD_API_URL + url)

            async with operation as res:
                # logger.debug(await res.text())
                # logger.debug(res.status)
                if res.status == 429:
                    json_res = await res.json()
                    limit = await RateLimit.from_api_res(json_res)
                    # TODO: Handle global rate limit?

                    if 'X-RateLimit-Remaining' in res.headers and int(res.headers['X-RateLimit-Remaining']) > 0:
                        logger.debug(
                            f"Status is {res.status} but i have {res.headers['X-RateLimit-Remaining']} ratelimits remaining, ")
                        continue

                    logger.debug(
                        f"Status is {res.status} so we must wait {limit.retry_after / 1000} seconds!")
                    await asyncio.sleep(limit.retry_after / 1000)
                    logger.debug("Done waiting! Requesting again")
                elif res.status < 300 and res.status >= 200:
                    return await res.json()
                elif res.status == 401:
                    raise AuthorizationError
                else:
                    raise UnhandledEndpointStatusError
