from .base import DiscordObject


class Channel(DiscordObject):
    """Represents a guild or DM channel within Discord."""

    def __init__(self, id=0, type=0, guild_id=0, position=0, permission_overwrites=[],
                 name="", topic="", nsfw=False, last_message_id=0,
                 bitrate=0, user_limit=0, recipients=[], icon="",
                 owner_id=0, application_id=0, parent_id=0, last_pin_timestamp=None):
        self.id = id
        self.type = type
        self.guild_id = guild_id
        self.position = position
        self.permission_overwrites = permission_overwrites
        self.name = name
        self.topic = topic
        self.nsfw = nsfw
        self.last_message_id = last_message_id
        self.bitrate = bitrate
        self.user_limit = user_limit
        self.recipients = recipients
        self.icon = icon
        self.owner_id = owner_id
        self.application_id = application_id
        self.parent_id = parent_id
        self.last_pin_timestamp = last_pin_timestamp


class MessageActivity(DiscordObject):
    def __init__(self, type=None, party_id=""):
        self.type = type
        self.party_id = party_id


class MessageApplication(DiscordObject):
    def __init__(self, id=0, cover_image="", description="", icon="", name=""):
        self.id = id
        self.cover_image = cover_image
        self.description = description
        self.icon = icon
        self.name = name


class ChannelMessage(DiscordObject):
    """Represents a message sent in a channel within Discord."""

    def __init__(self, id=0, channel_id=0, author=None, content="", timestamp=None,
                 edited_timestamp=None, tts=False, mention_everyone=False, mentions=[],
                 mention_roles=[], attachments=[], embeds=[], reactions=[],
                 nonce=0, pinned=False, webhook_id=0, type=0,
                 activity=MessageActivity(), application=MessageApplication()):
        self.id = id
        self.channel_id = channel_id
        self.author = author
        self.content = content
        self.timestamp = timestamp
        self.edited_timestamp = edited_timestamp
        self.tts = tts
        self.mention_everyone = mention_everyone
        self.mentions = mentions
        self.mention_roles = mention_roles
        self.attachments = attachments
        self.embeds = embeds
        self.reactions = reactions
        self.nonce = nonce
        self.pinned = pinned
        self.webhook_id = webhook_id
        self.type = type
        self.activity = activity
        self.application = application
