import aiohttp
import asyncio
import json
import time
import logging
import threading
import platform
from concurrent.futures import ProcessPoolExecutor

from .user import User, UserConnection
from .guild import Guild, GuildMember
from .base import DiscordObject
from .version import PYDISCORD_VERSION_STR
from .constants import DISCORD_API_URL
from .channel import Channel
from .exceptions import WebSocketCreationError
from .enums import GatewayOpcodes

FORMAT = '%(asctime)-15s: %(message)s'
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('DiscordClient')


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
        self.executor = ProcessPoolExecutor(2)
        self.discord_client = discord_client

    async def create_session(self):
        self.session = aiohttp.ClientSession(headers=self.headers, auto_decompress=True)

    async def close_session(self):
        await self.session.close()

    async def start_websocket_in_thread(self):
        #self.loop = asyncio.new_event_loop()
        await self.start_websocket()
        # self.loop.close()

    async def start_websocket(self):
        res = await self.request_url('/gateway/bot')
        if res.status == 200:
            info = await res.json()
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
                        if GatewayOpcodes(dct['op']) == GatewayOpcodes.HELLO:
                            if self.heartbeat_future is not None:
                                if not self.heartbeat_future.cancelled():
                                    self.heartbeat_future.cancel()
                                    self.heartbeat_future = None
                            self.heartbeat_interval = dct['d']['heartbeat_interval']
                            self._trace = dct['d']['_trace']
                            self.s = dct['s']
                            logger.debug('Ensuring heartbeat!')
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
                            self.heartbeat_future = asyncio.ensure_future(
                                self.send_heartbeat(ws))
                        elif GatewayOpcodes(dct['op']) == GatewayOpcodes.HEARTBEAT_ACK:
                            logger.debug("Got heartbeat")
                            self.s = dct['s']
                        elif GatewayOpcodes(dct['op']) == GatewayOpcodes.DISPATCH:
                            event_type = dct['t']
                            if event_type == 'READY':
                                self.session_id = dct['d']['session_id']
                                await self.discord_client.raise_event('on_ready', dct['d'])
        else:
            raise WebSocketCreationError()

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
                elif res.status < 300 and res.status >= 200:
                    return res
                elif res.status == 401:
                    logger.warning(
                        f"You requested a api endpoint which you have no authorization: {text}")
                    # TODO: Throw error here
                    return res
                else:
                    # TODO: Throw errors here
                    logger.warning(
                        f"Unhandled response status when requesting url = '{url}'")
                    return res
