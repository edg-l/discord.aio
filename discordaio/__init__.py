"""
discord.aio is an asynchronous Discord API wrapper for python 3.6+
"""

from .version import VERSION_STR

__author__ = 'Ryozuki'
__license__ = 'MIT'
__version__ = VERSION_STR

from .client import DiscordBot
from .channel import Channel, ChannelMessage, Attachment, Embed, EmbedAuthor, EmbedField, EmbedFooter, EmbedImage, EmbedProvider, EmbedThumbnail, EmbedVideo
from .emoji import Emoji
from .user import User, UserConnection
from .guild import Guild, GuildEmbed, GuildMember, Integration, IntegrationAccount
from .role import Role
from .invite import Invite, InviteMetadata
from .enums import ChannelTypes, ExplicitContentFilterLevel, MessageActivityTypes, MessageNotificationLevel, MFALevel, VerificationLevel
from .exceptions import WebSocketCreationError, AuthorizationError, EventTypeError, UnhandledEndpointStatusError
from .base import DiscordObject
from .voice import VoiceRegion, VoiceState