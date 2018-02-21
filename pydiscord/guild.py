import logging
import json

from .base import DiscordObject
from .user import User
from .emoji import Emoji
from .internal_util import get_class_list

FORMAT = '%(asctime)-15s: %(message)s'
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('DiscordClient')


class Role(DiscordObject):
    def __init__(self, id=0, name="", color=0, hoist=False, position=0,
                 permissions=0, managed=False, mentionable=False):
        self.id = id
        self.name = name
        self.color = color
        self.hoist = hoist
        self.position = position
        self.permissions = permissions
        self.managed = managed
        self.mentionable = mentionable


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

    @classmethod
    def from_dict(cls, dct: dict):
        obj = cls()
        for key, value in dct.items():
            if key == 'user':
                setattr(obj, key, User.from_dict(value))
            else:
                setattr(obj, key, value)
        return obj


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

    @classmethod
    def from_json(cls, text: str):
        obj = cls()
        json_text = json.loads(text)
        for key, value in json_text.items():
            if key == 'roles':
                setattr(obj, key, get_class_list(Role, value))
            elif key == 'members':
                setattr(obj, key, get_class_list(GuildMember, value))
            elif key == 'emojis':
                setattr(obj, key, get_class_list(Emoji, value))
            else:
                setattr(obj, key, value)
        return obj

    @classmethod
    def from_json_array(cls, text: str):
        objs = []
        json_text = json.loads(text)
        # print(json_text)
        for jobj in json_text:
            c = cls()
            for key, value in jobj.items():

                if key == 'roles':
                    setattr(c, key, get_class_list(Role, value))
                elif key == 'members':
                    setattr(c, key, get_class_list(GuildMember, value))
                else:
                    setattr(c, key, value)
            objs.append(c)
        return objs

    def _fill_members(self, json_text):
        members = json.loads(json_text)
        self.members = []
        for member in members:
            self.members.append(GuildMember.from_dict(member))

    def is_owner(self, member: GuildMember):
        return self.owner_id == member.user.id


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


class IntegrationAccount(DiscordObject):
    def __init__(self, id="", name=""):
        self.id = id
        self.name = name


class Ban(DiscordObject):
    def __init__(self, reason="", user=None):
        self.reason = reason
        self.user = user
