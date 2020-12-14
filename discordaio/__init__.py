"""
discord.aio is an asynchronous Discord API wrapper for python 3.6+
"""

from .client import DiscordBot
from .channel import Channel, ChannelMessage, Attachment, Embed, EmbedAuthor, EmbedField, EmbedFooter, \
    EmbedImage, EmbedProvider, EmbedThumbnail, EmbedVideo
from .emoji import Emoji
from .user import User, UserConnection
from .guild import Guild, GuildEmbed, GuildMember, Integration, IntegrationAccount
from .role import Role
from .http import HTTPHandler
from .websocket import DiscordWebsocket
from .webhook import Webhook
from .invite import Invite
from .enums import ChannelTypes, ExplicitContentFilterLevel, MessageActivityTypes, MessageNotificationLevel, \
    MFALevel, VerificationLevel
from .exceptions import WebSocketCreationError, AuthorizationError, EventTypeError, UnhandledEndpointStatusError
from .base import DiscordObject
from .voice import VoiceRegion, VoiceState
from .activity import Activity, ActivityAssets, ActivityParty, ActivityTimestamps
from .constants import DISCORD_API_URL, DISCORD_CDN
from .version import __version__

__author__ = 'Edgar <git@edgarluque.com>'
__license__ = 'MIT'
