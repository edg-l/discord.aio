from enum import Enum, unique


@unique
class MessageNotificationLevel(Enum):
    ALL_MESSAGES = 0
    ONLY_MENTIONS = 1


@unique
class ExplicitContentFilterLevel(Enum):
    DISABLED = 0
    MEMBERS_WITHOUT_ROLES = 1
    ALL_MEMBERS = 2


@unique
class MFALevel(Enum):
    NONE = 0
    ELEVATED = 1


@unique
class VerificationLevel(Enum):
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    VERY_HIGH = 4


@unique
class ChannelTypes(Enum):
    GUILD_TEXT = 0
    DM = 1
    GUILD_VOICE = 2
    GROUP_DM = 3
    GUILD_CATEGORY = 4


@unique
class MessageActivityTypes(Enum):
    JOIN = 1
    SPECTATE = 2
    LISTEN = 3
    JOIN_REQUEST = 5


@unique
class GatewayOpcodes(Enum):
    DISPATCH = 0
    HEARTBEAT = 1
    IDENTIFY = 2
    STATUS_UPDATE = 3
    VOICE_STATE_UPDATE = 4
    VOICE_SERVER_PING = 5
    RESUME = 6
    RECONNECT = 7
    REQUEST_GUILD_MEMBERS = 8
    INVALID_SESSION = 9
    HELLO = 10
    HEARTBEAT_ACK = 11


@unique
class ActivityTypes(Enum):
    GAME = 0
    STREAMING = 1
    LISTENING = 2


__all__ = [
    'MessageNotificationLevel',
    'ExplicitContentFilterLevel',
    'MFALevel',
    'VerificationLevel',
    'ChannelTypes',
    'MessageActivityTypes',
    'GatewayOpcodes',
]
