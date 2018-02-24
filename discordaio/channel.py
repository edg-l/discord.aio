"""Contains all related Channel Discord objects"""

from .base import DiscordObject
from .user import User
from .role import Role
from .emoji import Emoji


class Overwrite(DiscordObject):
    def __init__(self, id=0, type="", allow=0, deny=0):
        self.id = id
        self.type = type
        self.allow = allow
        self.deny = deny


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

    async def _from_api_ext(self, key, value):
        if key == 'recipients':
            setattr(self, key, [await User.from_api_res(x) for x in value])
        elif key == 'permission_overwrites':
            setattr(self, key, [await Overwrite.from_api_res(x) for x in value])
        else:
            return await super()._from_api_ext(key, value)
    
    def __str__(self):
        return f'{self.name}#{self.id}'

    def __repr__(self):
        return f'<Channel Object: {self.name}#{self.id}>'


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


class Reaction(DiscordObject):
    def __init__(self, count=0, me=False, emoji=None):
        self.count = count
        self.me = me
        self.emoji = emoji

    async def _from_api_ext(self, key, value):
        if key == 'emoji':
            setattr(self, key, await Emoji.from_api_res(value))
        else:
            return await super()._from_api_ext(key, value)


class EmbedThumbnail(DiscordObject):
    def __init__(self, url="", proxy_url="", height=0, width=0):
        self.url = url
        self.proxy_url = proxy_url
        self.height = height
        self.width = width


class EmbedVideo(DiscordObject):
    def __init__(self, url="", height=0, width=0):
        self.url = url
        self.height = height
        self.width = width


class EmbedImage(DiscordObject):
    def __init__(self, url="", proxy_url="", height=0, width=0):
        self.url = url
        self.proxy_url = proxy_url
        self.height = height
        self.width = width


class EmbedProvider(DiscordObject):
    def __init__(self, name="", url=""):
        self.name = name
        self.url = url


class EmbedAuthor(DiscordObject):
    def __init__(self, name="", url="", icon_url="", proxy_icon_url=""):
        self.name = name
        self.url = url
        self.icon_url = icon_url
        self.proxy_icon_url = proxy_icon_url


class EmbedFooter(DiscordObject):
    def __init__(self, text="", icon_url="", proxy_icon_url=""):
        self.text = text
        self.icon_url = icon_url
        self.proxy_icon_url = proxy_icon_url


class EmbedField(DiscordObject):
    def __init__(self, name="", value="", inline=False):
        self.name = name
        self.value = value
        self.inline = inline


class Embed(DiscordObject):
    def __init__(self, title="", type="", description="", url="", timestamp=None,
                 color=0, footer=EmbedFooter(), image=EmbedImage(), thumbnail=EmbedThumbnail(),
                 video=EmbedVideo(), provider=EmbedProvider(), author=EmbedAuthor(), fields=[]):
        self.title = title
        self.type = type
        self.description = description
        self.url = url
        self.timestamp = timestamp
        self.color = color
        self.footer = footer
        self.image = image
        self.thumbnail = thumbnail
        self.video = video
        self.provider = provider
        self.author = author
        self.fields = fields

    async def _from_api_ext(self, key, value):
        if key == 'footer':
            setattr(self, key, await EmbedFooter.from_api_res(value))
        elif key == 'image':
            setattr(self, key, await EmbedImage.from_api_res(value))
        elif key == 'thumbnail':
            setattr(self, key, await EmbedThumbnail.from_api_res(value))
        elif key == 'video':
            setattr(self, key, await EmbedVideo.from_api_res(value))
        elif key == 'provider':
            setattr(self, key, await EmbedProvider.from_api_res(value))
        elif key == 'author':
            setattr(self, key, await EmbedAuthor.from_api_res(value))
        elif key == 'fields':
            setattr(self, key, [await EmbedField.from_api_res(x) for x in value])
        else:
            return await super()._from_api_ext(key, value)


class Attachment(DiscordObject):
    def __init__(self, id=0, filename="", size=0, url="", proxy_url="",
                 height=0, width=0):
        self.id = id
        self.filename = filename
        self.size = size
        self.url = url
        self.proxy_url = proxy_url
        self.height = height
        self.width = width


class ChannelMessage(DiscordObject):
    """Represents a message sent in a channel within Discord.

    The author object follows the structure of the user object, but is only a valid user in the case where the message is generated by a user or bot user. 
    If the message is generated by a webhook, the author object corresponds to the webhook's id, username, and avatar. 
    You can tell if a message is generated by a webhook by checking for the webhook_id on the message object."""

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

    async def _from_api_ext(self, key, value):
        if key == 'author':
            setattr(self, key, await User.from_api_res(value))
        elif key == 'mentions':
            setattr(self, key, [await User.from_api_res(x) for x in value])
        elif key == 'mention_roles':
            setattr(self, key, [await Role.from_api_res(x) for x in value])
        elif key == 'attachments':
            setattr(self, key, [await Attachment.from_api_res(x) for x in value])
        elif key == 'reactions':
            setattr(self, key, [await Reaction.from_api_res(x) for x in value])
        elif key == 'activity':
            setattr(self, key, await MessageActivity.from_api_res(value))
        elif key == 'activity':
            setattr(self, key, await MessageApplication.from_api_res(value))
        else:
            return await super()._from_api_ext(key, value)
