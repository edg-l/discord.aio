"""Contains all related Channel Discord objects"""

from .base import DiscordObject
from .user import User
from .role import Role
from .emoji import Emoji


class Overwrite(DiscordObject):
    """Represents a Overwrite object.

    .. versionadded:: 0.2.0

    Attributes:
        id (:obj:`int`): role or user id
        type (:obj:`str`): either "role" or "member"
        allow (:obj:`int`): permission bit set
        deny (:obj:`int`): permission bit set
    """

    def __init__(self, id=0, type="", allow=0, deny=0):
        self.id = id
        self.type = type
        self.allow = allow
        self.deny = deny


class Channel(DiscordObject):
    """Represents a guild or DM channel within Discord.

    .. versionadded:: 0.2.0

    Attributes:
        id (:obj:`int`): the id of this channel
        value_type (:obj:`int`): the value_type of channel
        guild_id (:obj:`int`, optional): the id of the guild
        position (:obj:`int`, optional): sorting position of the channel
        permission_overwrites (:obj:`list` of :class:`.Overwrite`, optional): explicit permission overwrites for members and roles
        name (:obj:`str`, optional): the name of the channel (2-100 characters)
        topic (:obj:`str`, optional): the channel topic (0-1024 characters)
        nsfw (:obj:`bool`, optional): if the channel is nsfw
        last_message_id (:obj:`int`, optional): the id of the last message sent in this channel (may not point to an existing or valid message)
        bitrate (:obj:`int`, optional): the bitrate (in bits) of the voice channel
        user_limit (:obj:`int`, optional): the user limit of the voice channel
        recipients (:obj:`list` of :class:`.User`, optional): the recipients of the DM
        icon (:obj:`str`, optional): icon hash
        owner_id (:obj:`int`, optional): id of the DM creator
        application_id (:obj:`int`, optional): application id of the group DM creator if it is bot-created
        parent_id (:obj:`int`, optional): id of the parent category for a channel
        last_pin_timestamp (:obj:`int`, optional): timestamp when the last pinned message was pinned
    """

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
    """Represents a Message Activity.

    .. versionadded:: 0.2.0

    Attributes:
        type (:obj:`int`): type of message activity
        party_id (:obj:`str`, optional): party_id from a Rich Presence event
    """

    def __init__(self, type=None, party_id=""):
        self.type = type
        self.party_id = party_id


class MessageApplication(DiscordObject):
    """Represents a Message Application.

    .. versionadded:: 0.2.0

    Attributes:
        id (:obj:`int`): id of the application
        cover_image (:obj:`str`): id of the embed's image asset
        description (:obj:`str`): application's description
        icon (:obj:`str`): id of the application's icon
        name (:obj:`str`): name of the application
    """

    def __init__(self, id=0, cover_image="", description="", icon="", name=""):
        self.id = id
        self.cover_image = cover_image
        self.description = description
        self.icon = icon
        self.name = name


class Reaction(DiscordObject):
    """Represents a Reaction.

    .. versionadded:: 0.2.0

    Attributes:
        count (:obj:`int`): times this emoji has been used to react
        me (:obj:`bool`): whether the current user reacted using this emoji
        emoji (:class:`.Emoji`): emoji information
    """

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
    """Represents a embed thumbnail object

    .. versionadded:: 0.2.0

    Attributes:
        url (:obj:`str`): source url of thumbnail (only supports http(s) and attachments)
        proxy_url (:obj:`str`): a proxied url of the thumbnail
        height (:obj:`int`): height of thumbnail
        width (:obj:`int`): width of thumbnail
    """

    def __init__(self, url="", proxy_url="", height=0, width=0):
        self.url = url
        self.proxy_url = proxy_url
        self.height = height
        self.width = width


class EmbedVideo(DiscordObject):
    """Represents a embed video

    .. versionadded:: 0.2.0

    Attributes:
        url (:obj:`str`): source url of video
        height (:obj:`int`): height of video
        width (:obj:`int`): width of video
    """

    def __init__(self, url="", height=0, width=0):
        self.url = url
        self.height = height
        self.width = width


class EmbedImage(DiscordObject):
    """Represents a embed image

    .. versionadded:: 0.2.0

    Attributes:
        url (:obj:`str`): source url of image (only supports http(s) and attachments)
        proxy_url (:obj:`str`): a proxied url of the image
        height (:obj:`int`): height of image
        width (:obj:`int`): width of image
    """

    def __init__(self, url="", proxy_url="", height=0, width=0):
        self.url = url
        self.proxy_url = proxy_url
        self.height = height
        self.width = width


class EmbedProvider(DiscordObject):
    """Represents a embed provider

    .. versionadded:: 0.2.0

    Attributes:
        name (:obj:`str`): name of provider
        url (:obj:`str`): url of provider
    """

    def __init__(self, name="", url=""):
        self.name = name
        self.url = url


class EmbedAuthor(DiscordObject):
    """Represents a embed author

    .. versionadded:: 0.2.0

    Attributes:
        name (:obj:`str`): name of author
        url (:obj:`str`): url of author
        icon_url (:obj:`str`): url of author icon (only supports http(s) and attachments)
        proxy_icon_url (:obj:`str`): a proxied url of author icon
    """

    def __init__(self, name="", url="", icon_url="", proxy_icon_url=""):
        self.name = name
        self.url = url
        self.icon_url = icon_url
        self.proxy_icon_url = proxy_icon_url


class EmbedFooter(DiscordObject):
    """Represents a embed footer

    .. versionadded:: 0.2.0

    Attributes:
        text (:obj:`str`): footer text
        icon_url (:obj:`str`): url of footer icon (only supports http(s) and attachments)
        proxy_icon_url (:obj:`str`): a proxied url of footer icon
    """

    def __init__(self, text="", icon_url="", proxy_icon_url=""):
        self.text = text
        self.icon_url = icon_url
        self.proxy_icon_url = proxy_icon_url


class EmbedField(DiscordObject):
    """Represents a embed field

    .. versionadded:: 0.2.0

    Attributes:
        name (:obj:`str`): name of the field
        value (:obj:`str`): value of the field
        inline (:obj:`bool`): whether or not this field should display inline
    """

    def __init__(self, name="", value="", inline=False):
        self.name = name
        self.value = value
        self.inline = inline


class Embed(DiscordObject):
    """Represents a discord Embed

    .. versionadded:: 0.2.0

    Attributes:
        title (:obj:`str`): title of embed
        type (:obj:`str`): type of embed (always "rich" for webhook embeds)
        description (:obj:`str`): description of embed
        url (:obj:`str`): url of embed
        timestamp (:obj:`int`): timestamp of embed content
        color (:obj:`int`): color code of the embed
        footer (:class:`.EmbedFooter`): footer information
        image (:class:`.EmbedImage`): image information
        thumbnail (:class:`.EmbedThumbnail`): thumbnail information
        video (:class:`.EmbedVideo`): video information
        provider (:class:`.EmbedProvider`): provider information
        author (:class:`.EmbedAuthor`): author information
        fields (:obj:`list` of :class:`.EmbedField`): fields information
    """

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
    """Represents a attachment

    .. versionadded:: 0.2.0

    Attributes:
        id (:obj:`int`): attachment id
        filename (:obj:`str`): name of file attached
        size (:obj:`int`): size of file in bytes
        url (:obj:`str`): source url of file
        proxy_url (:obj:`str`): a proxied url of file
        height (:obj:`int`): height of file (if image)
        width (:obj:`int`): width of file (if image)
    """

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

    .. versionadded:: 0.2.0

    Note:
        The author object follows the structure of the :class:`.User` object, but is only a valid user in the case where the message is generated by a user or bot user.
        If the message is generated by a :class:`.Webhook`, the author object corresponds to the webhook's id, username, and avatar.
        You can tell if a message is generated by a webhook by checking for the webhook_id on the message object.

    Attributes:
        id (:obj:`int`): id of the message
        channel_id (:obj:`int`): id of the channel the message was sent in
        author (user): object the author of this message (not guaranteed to be a valid user, see below)
        content (:obj:`str`): contents of the message
        timestamp (:obj:`int`): timestamp when this message was sent
        edited_timestamp (:obj:`int`): timestamp when this message was edited (or null if never)
        tts (:obj:`bool`): whether this was a TTS message
        mention_everyone (:obj:`bool`): whether this message mentions everyone
        mentions (:obj:`list` of :class:`.User`): objects users specifically mentioned in the message
        mention_roles (:obj:`list` of :class:`.Role`): object ids roles specifically mentioned in this message
        attachments (:obj:`list` of :class:`.Attachment`): objects any attached files
        embeds (:obj:`list` of :class:`.Embed`): objects any embedded content
        reactions (:obj:`list` of :class:`.Reaction`): objects reactions to the message
        nonce (:obj:`int`, optional): used for validating a message was sent
        pinned (:obj:`bool`): whether this message is pinned
        webhook_id (:obj:`int`, optional): if the message is generated by a webhook, this is the webhook's id
        type (:obj:`int`): type of message
        activity (MessageActivity): activity object sent with Rich Presence-related chat embeds
        application (MessageApplication): application object sent with Rich Presence-related chat embeds
    """

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


__all__ = [
    'Channel',
    'ChannelMessage',
    'Overwrite',
    'MessageActivity',
    'MessageApplication',
    'Reaction',
    'Embed',
    'EmbedThumbnail',
    'EmbedVideo',
    'EmbedImage',
    'EmbedProvider',
    'EmbedAuthor',
    'EmbedFooter',
    'EmbedField',
    'Attachment',
]
