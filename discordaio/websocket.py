import asyncio
import aiohttp
import json
import platform

from .enums import GatewayOpcodes
from .guild import Guild, GuildMember
from .user import User
from .http import HTTPHandler
from .role import Role
from .channel import Channel, ChannelMessage
from .emoji import Emoji
from .activity import Activity
from .voice import VoiceState

import logging

logger = logging.getLogger(__name__)


class DiscordWebsocket:
    """Class used for handling the websocket connection with the discord gateway

    .. versionadded:: 0.2.0

    Attributes:
        heartbeat_interval (:obj:`float`): The interval to send pings
        _trace (:obj:`str`): Used for debugging
        seq (:obj:`str`): Used in pings
        session_id (:obj:`str`): Used for resuming
        http (:class:`HTTPHandler`): Used for sending http requests and session handling.
        gateway_url (:obj:`str`): The gateway url
        shards (:obj:`list` of :obj:`int`): Used for opening multiple connections
        ws (:class:aiohttp.ClientWebSocketResponse``): The websocket
    """

    def __init__(self, http: HTTPHandler = None, session_id: str = None, shards: list = []):
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
            logger.debug(f'Waiting {self.heartbeat_interval / 1000} seconds to send heartbeat')
            await asyncio.sleep(self.heartbeat_interval / 1000)
            await self.ws.send_json({
                'op': 1,
                'd': self.seq
            })
            logger.debug("Sent heartbeat")

    async def close(self) -> bool:
        """Closes the websocket

        .. versionadded:: 0.2.0

        Returns:
            bool: True if succeeded closing. False if the websocket was already closed
        """
        if self.ws is not None and not self.ws.closed:
            if self.heartbeat_future is not None and not self.heartbeat_future.cancelled():
                self.heartbeat_future.cancel()
            await self.ws.close()
            logger.debug('Websocket closed!')
            return True
        else:
            return False

    async def start(self):
        """Starts the websocket

        .. versionadded:: 0.2.0
        """
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
                        logger.debug(f'Ensuring to heartbeat every {self.heartbeat_interval / 1000} seconds!')
                        self.heartbeat_future = asyncio.ensure_future(self.send_heartbeat())
                    elif GatewayOpcodes(opcode) == GatewayOpcodes.HEARTBEAT_ACK:
                        logger.debug(f'Got HEARTBEAT_ACK (new s: {dct["s"]}, old s: {self.seq})')
                        self.seq = dct['s']
                    elif GatewayOpcodes(opcode) == GatewayOpcodes.DISPATCH:
                        event_type = dct['t']
                        asyncio.ensure_future(self.dispatch_event(event_type, data))

    async def dispatch_event(self, event, data):
        if event == 'READY':
            self.session_id = data['session_id']
            self.http.get_client().user = await User.from_api_res(data['user'])
            self.http.get_client().guilds = await Guild.from_api_res(data['guilds'])
            return await self.http.get_client().raise_event('on_ready')

        elif event == 'RESUMED':
            return await self.http.get_client().raise_event('on_resumed')

        elif event == 'INVALID_SESSION':
            return await self.http.get_client().raise_event('on_invalid_session', data)

        elif event == 'CHANNEL_CREATE':
            return await self.http.get_client().raise_event('on_channel_create', await Channel.from_api_res(data))

        elif event == 'CHANNEL_UPDATE':
            return await self.http.get_client().raise_event('on_channel_update', await Channel.from_api_res(data))

        elif event == 'CHANNEL_DELETE':
            return await self.http.get_client().raise_event('on_channel_delete', await Channel.from_api_res(data))

        elif event == 'CHANNEL_PINS_UPDATE':
            return await self.http.get_client().raise_event('on_channel_pin', data['channel_id'],
                                                            data['last_pin_timestamp'])

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

        elif event == 'GUILD_EMOJIS_UPDATE':
            guild_id = data['guild_id']
            return await self.http.get_client().raise_event('on_guild_emojis_update', guild_id,
                                                            await Emoji.from_api_res(data['emojis']))

        elif event == 'GUILD_INTEGRATIONS_UPDATE':
            guild_id = data['guild_id']
            return await self.http.get_client().raise_event('on_guild_integrations_update', guild_id)

        elif event == 'GUILD_MEMBER_ADD':
            guild_id = data['guild_id']
            return await self.http.get_client().raise_event('on_guild_member_add', guild_id,
                                                            await GuildMember.from_api_res(data))

        elif event == 'GUILD_MEMBER_REMOVE':
            guild_id = data['guild_id']
            return await self.http.get_client().raise_event('on_guild_member_remove', guild_id,
                                                            await User.from_api_res(data['user']))

        elif event == 'GUILD_MEMBER_UPDATE':
            guild_id = data['guild_id']
            return await self.http.get_client().raise_event('on_guild_member_update', guild_id,
                                                            await Role.from_api_res(data['roles']),
                                                            await User.from_api_res(data['user']), data['nick'])

        elif event == 'GUILD_MEMBERS_CHUNK':
            guild_id = data['guild_id']
            return await self.http.get_client().raise_event('on_guild_members_chunk', guild_id,
                                                            await GuildMember.from_api_res(data['members']))

        elif event == 'GUILD_ROLE_CREATE':
            guild_id = data['guild_id']
            return await self.http.get_client().raise_event('on_guild_role_create', guild_id,
                                                            await Role.from_api_res(data['role']))

        elif event == 'GUILD_ROLE_UPDATE':
            guild_id = data['guild_id']
            return await self.http.get_client().raise_event('on_guild_role_update', guild_id,
                                                            await Role.from_api_res(data['role']))

        elif event == 'GUILD_ROLE_DELETE':
            guild_id = data['guild_id']
            return await self.http.get_client().raise_event('on_guild_role_delete', guild_id, data['role_id'])

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

        elif event == 'PRESENCE_UPDATE':
            await self.http.get_client().raise_event('on_presence_update', await User.from_api_res(data['user']),
                                                     data['roles'], await Activity.from_api_res(data.get('game')),
                                                     data['guild_id'],
                                                     data['status'])

        elif event == 'TYPING_START':
            await self.http.get_client().raise_event('on_typing_start', data['user_id'], data['channel_id'],
                                                     data['timestamp'])

        elif event == 'USER_UPDATE':
            await self.http.get_client().raise_event('on_user_update', await User.from_api_res(data))

        elif event == 'VOICE_STATE_UPDATE':
            await self.http.get_client().raise_event('on_voice_state_update', await VoiceState.from_api_res(data))

        elif event == 'VOICE_SERVER_UPDATE':
            await self.http.get_client().raise_event('on_voice_server_update', data['token'], data['guild_id'],
                                                     data['endpoint'])

        elif event == 'WEBHOOKS_UPDATE':
            await self.http.get_client().raise_event('on_webhooks_update', data['guild_id'], data['channel_id'])

        else:
            logger.critical(
                f'Unhandled event type {event}, data: {data}')


__all__ = [
    'DiscordWebsocket',
]
