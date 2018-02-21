from .base import DiscordObject


class GuildEmbed(DiscordObject):
    """A Guild Embed Object"""

    def __init__(self, enabled=False, channel_id=0):
        self.enabled = enabled
        self.channel_id = channel_id


class GuildMember(DiscordObject):
    def __init__(self, user=None, nick="", roles=[], joined_at=None, deaf=False,
                 mute=False):
        self.user = user
        self.nick = nick
        self.roles = roles
        self.joined_at = joined_at
        self.deaf = deaf
        self.mute = mute


class Guild(DiscordObject):
    """A Discord Guild Object"""

    def __init__(self, id=0, name="", icon="", splash="", owner=False,
                 owner_id=0, permissions=0, region="", afk_channel_id=0,
                 afk_timeout=0, embed_enabled=False, embed_channel_id=0, verification_level=0,
                 default_message_notifications=0, explicit_content_filter=0, roles=[], emojis=[],
                 features=[], mfa_level=0, application_id=0, widget_enabled=False,
                 widget_channel_id=0, system_channel_id=0, joined_at=None, large=None,
                 unavailable=None, member_count=None, voice_states=None, members=None,
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
