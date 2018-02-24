import asyncio
import aiohttp
import json
import platform

from .enums import GatewayOpcodes
from .guild import Guild
from .user import User
from .http import HTTPHandler
from .channel import Channel, ChannelMessage
from .emoji import Emoji

import logging
logger = logging.getLogger(__name__)


class DiscordWebsocket:
    def __init__(self, http: HTTPHandler=None, session_id: str=None, shards: list=[]):
        self.heartbeat_interval: float = None
        self._trace: list = []
        self.seq: str = None
        self.heartbeat_future: asyncio.Future = None
        self.session_id: str = session_id
        self.http: HTTPHandler = http
        self.gateway_url: str = None
        self.shards: list = shards
        self.ws: aiohttp.ClientWebSocketResponse = None

    @property
    def closed(self) -> bool:
        return self.ws is None or self.ws.closed

    async def send_heartbeat(self):
        while True:
            if self.ws is None or self.ws.closed:
                break
            logger.debug(
                f'Waiting {self.heartbeat_interval / 1000} seconds to send heartbeat')
            await asyncio.sleep(self.heartbeat_interval / 1000)
            await self.ws.send_json({
                'op': 1,
                'd': self.s
            })
            logger.debug("Sent heartbeat")

    async def close(self) -> bool:
        if self.ws is not None and not self.ws.closed:
            if self.heartbeat_future is not None and not self.heartbeat_future.cancelled():
                self.heartbeat_future.cancel()
            await self.ws.close()
            logger.debug('Websocket closed!')
            return True
        else:
            return False

    async def start(self):
        if self.ws is not None and not self.ws.closed:
            await self.ws.close()
            self.ws = None

        info = await self.http.request_url('/gateway/bot')
        self.gateway_url = info['url']
        self.shards = info['shards']

        logger.debug(f'I can use {self.shards} shards!')

        async with self.http.session.ws_connect(self.gateway_url + '?v=6&encoding=json') as ws:
            self.ws = ws
            async for msg in self.ws:
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
                        self.seq = dct['s']
                        if self.session_id is not None:
                            pass
                            await ws.send_json({
                                "op": 6,  # Resume
                                "d": {
                                    "token": self.http.token,
                                    "session_id": self.session_id,
                                    "seq": self.seq
                                }
                            })
                        else:
                            await ws.send_json({
                                "op": 2,  # Identify
                                "d": {
                                    "token": self.http.token,
                                    "properties": {
                                        '$os': platform.system(),
                                        '$browser': 'discord.aio',
                                        '$device': 'discord.aio'
                                    },
                                    "compress": False,
                                    "large_threshold": 250
                                }
                            })
                        logger.debug(
                            f'Ensuring to heartbeat every {self.heartbeat_interval / 1000} seconds!')
                        self.heartbeat_future = asyncio.ensure_future(
                            self.send_heartbeat())
                    elif GatewayOpcodes(opcode) == GatewayOpcodes.HEARTBEAT_ACK:
                        logger.debug(
                            f'Got HEARTBEAT_ACK (new s: {dct["s"]}, old s: {self.seq})')
                        self.s = dct['s']
                    elif GatewayOpcodes(opcode) == GatewayOpcodes.DISPATCH:
                        event_type = dct['t']
                        asyncio.ensure_future(
                            self.dispatch_event(event_type, data))

    async def dispatch_event(self, event, data):
        if event == 'READY':
            self.session_id = data['session_id']
            self.http.get_client().user = await User.from_api_res(data['user'])
            self.http.get_client().guilds = await Guild.from_api_res(data['guilds'])
            asyncio.ensure_future(
                self.http.get_client().raise_event('on_ready'))

        elif event == 'GUILD_CREATE':
            guild = await Guild.from_api_res(data)
            return await self.http.get_client().raise_event('on_guild_create', guild)

        elif event == 'GUILD_DELETE':
            guild = await Guild.from_api_res(data)
            return await self.http.get_client().raise_event('on_guild_delete', guild)

        elif event == 'GUILD_BAN_ADD':
            guild_id = data['guild_id']
            return await self.http.get_client().raise_event('on_ban', guild_id, await User.from_api_res(data))

        elif event == 'GUILD_BAN_REMOVE':
            guild_id = data['guild_id']
            return await self.http.get_client().raise_event('on_ban_remove', guild_id, await User.from_api_res(data))

        elif event == 'TYPING_START':
            await self.http.get_client().raise_event('on_typing_start', data['user_id'], data['channel_id'], data['timestamp'])

        elif event == 'MESSAGE_CREATE':
            message = await ChannelMessage.from_api_res(data)
            await self.http.get_client().raise_event('on_message', message)

        elif event == 'MESSAGE_UPDATE':
            message = await ChannelMessage.from_api_res(data)
            await self.http.get_client().raise_event('on_message_create', message)

        elif event == 'MESSAGE_DELETE':
            await self.http.get_client().raise_event('on_message_delete', data['id'], data['channel_id'])

        elif event == 'MESSAGE_DELETE_BULK':
            await self.http.get_client().raise_event('on_message_delete_bulk', data['ids'], data['channel_id'])

        elif event == 'MESSAGE_REACTION_ADD':
            emoji = await Emoji.from_api_res(data['emoji'])
            await self.http.get_client().raise_event(
                'on_message_reaction_add', data['user_id'], data['channel_id'], data['message_id'], emoji)

        elif event == 'MESSAGE_REACTION_REMOVE':
            emoji = await Emoji.from_api_res(data['emoji'])
            await self.http.get_client().raise_event(
                'on_message_reaction_remove', data['user_id'], data['channel_id'], data['message_id'], emoji)

        elif event == 'MESSAGE_REACTION_REMOVE_ALL':
            await self.http.get_client().raise_event(
                'on_message_reaction_remove_all', data['channel_id'], data['message_id'])

        else:
            logger.critical(
                f'Unhandled event type {event}, data: {data}')
