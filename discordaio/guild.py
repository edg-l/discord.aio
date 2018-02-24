import json

from .base import DiscordObject
from .user import User
from .emoji import Emoji
from .constants import DISCORD_CDN
from .channel import Channel
from .role import Role

import logging
logger = logging.getLogger(__name__)


class GuildEmbed(DiscordObject):
    """A Guild Embed Object"""

    def __init__(self, enabled=False, channel_id=0):
        self.enabled = enabled
        self.channel_id = channel_id


class GuildMember(DiscordObject):
    def __init__(self, user=User(), nick="", roles=[], joined_at=None, deaf=False,
                 mute=False):
        self.user = user
        self.nick = nick
        self.roles = roles
        self.joined_at = joined_at
        self.deaf = deaf
        self.mute = mute

    async def _from_api_ext(self, key, value):
        if key == 'user':
            setattr(self, key, await User.from_api_res(value))
        else:
            await super()._from_api_ext(key, value)

    def __str__(self):
        return self.user.__str__()

    def __repr__(self):
        return f'<GuildMember Object: {self.user.username}#{self.user.discriminator}>'


class Guild(DiscordObject):
    """A Discord Guild Object"""

    def __init__(self, id=0, name="", icon="", splash="", owner=False,
                 owner_id=0, permissions=0, region="", afk_channel_id=0,
                 afk_timeout=0, embed_enabled=False, embed_channel_id=0, verification_level=0,
                 default_message_notifications=0, explicit_content_filter=0, roles=[], emojis=[],
                 features=[], mfa_level=0, application_id=0, widget_enabled=False,
                 widget_channel_id=0, system_channel_id=0, joined_at=None, large=None,
                 unavailable=None, member_count=None, voice_states=None, members=[],
                 channels=None, presences=None):
        self.id = id
        self.name = name
        self.icon = icon
        self.splash = splash
        self.owner = owner
        self.owner_id = owner_id
        self.permissions = permissions
        self.region = region
        self.afk_channel_id = afk_channel_id
        self.afk_timeout = afk_timeout
        self.embed_enabled = embed_enabled
        self.embed_channel_id = embed_channel_id
        self.verification_level = verification_level
        self.default_message_notifications = default_message_notifications
        self.explicit_content_filter = explicit_content_filter
        self.roles = roles
        self.emojis = emojis
        self.features = features
        self.mfa_level = mfa_level
        self.application_id = application_id
        self.widget_enabled = widget_enabled
        self.widget_channel_id = widget_channel_id
        self.system_channel_id = system_channel_id
        self.joined_at = joined_at
        self.large = large
        self.unavailable = unavailable
        self.member_count = member_count
        self.voice_states = voice_states
        self.members = members
        self.channels = channels
        self.presences = presences

    async def _from_api_ext(self, key, value):
        if key == 'roles':
            setattr(self, key, [await Role.from_api_res(x) for x in value])
            pass
        elif key == 'members':
            setattr(self, key, [await GuildMember.from_api_res(x) for x in value])
            pass
        elif key == 'emojis':
            setattr(self, key, [await Emoji.from_api_res(x) for x in value])
            pass
        elif key == 'channels':
            setattr(self, key, [await Channel.from_api_res(x) for x in value])
            pass
        else:
            await super()._from_api_ext(key, value)

    async def _fill_members(self, members: list):
        self.members = []
        for member in members:
            self.members.append(await GuildMember.from_api_res(member))

    def is_owner(self, member: GuildMember):
        return self.owner_id == member.user.id

    def get_icon(self):
        return DISCORD_CDN + f'/icons/{self.id}/{self.icon}.png'

    def get_splash(self):
        return DISCORD_CDN + f'/splashes/{self.id}/{self.splash}.png'

    def __str__(self):
        return f'{self.name}#{self.id}'

    def __repr__(self):
        return f'<Guild Object: {self.name}#{self.id}>'


class IntegrationAccount(DiscordObject):
    def __init__(self, id="", name=""):
        self.id = id
        self.name = name


class Integration(DiscordObject):
    def __init__(self, id=0, name="", type="", enabled=False, syncing=False,
                 role_id=0, expire_behavior=0, expire_grace_period=0, user=None,
                 account=None, synced_at=None):
        self.id = id
        self.name = name
        self.type = type
        self.enabled = enabled
        self.syncing = syncing
        self.role_id = role_id
        self.expire_behavior = expire_behavior
        self.expire_grace_period = expire_grace_period
        self.user = user
        self.account = account
        self.synced_at = synced_at

    async def _from_api_ext(self, key, value):
        if key == 'user':
            setattr(self, key, await User.from_api_res(value))
        elif key == 'account':
            setattr(self, key, await IntegrationAccount.from_api_res(value))
        else:
            return await super()._from_api_ext(key, value)


class Ban(DiscordObject):
    def __init__(self, reason="", user=None):
        self.reason = reason
        self.user = user
    
    async def _from_api_ext(self, key, value):
        if key == 'user':
            setattr(self, key, await User.from_api_res(value))
        else:
            return await super()._from_api_ext(key, value)
