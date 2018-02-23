"""
PyDiscord, a discord api wrapper for python 3.6+
"""

from .version import PYDISCORD_VERSION_STR

__author__ = 'Ryozuki'
__license__ = 'MIT'
__version__ = PYDISCORD_VERSION_STR

from .client import DiscordBot
from .channel import Channel, ChannelMessage, Attachment, Embed, EmbedAuthor, EmbedField, EmbedFooter, EmbedImage, EmbedProvider, EmbedThumbnail, EmbedVideo
from .emoji import Emoji
from .user import User, UserConnection
from .guild import Guild, GuildEmbed, GuildMember, Integration, IntegrationAccount
from .invite import Invite, InviteMetadata
from .enums import ChannelTypes, ExplicitContentFilterLevel, MessageActivityTypes, MessageNotificationLevel, MFALevel, VerificationLevel
from .version import PYDISCORD_VERSION_STR
from .exceptions import WebSocketCreationError, AuthorizationError, EventTypeError, UnhandledEndpointStatusError
from .base import DiscordObject