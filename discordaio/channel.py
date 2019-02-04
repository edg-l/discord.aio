"""Contains all related Channel Discord objects"""

from .base import DiscordObject
from .user import User
from .role import Role
from .emoji import Emoji
from .invite import Invite
from typing import List
from enum import Enum


class Overwrite(DiscordObject):
    """Represents a Overwrite object.

    .. versionadded:: 0.2.0

    Attributes:
        id (:obj:`int`): role or user id
        type (:obj:`str`): either "role" or "member"
        allow (:obj:`int`): permission bit set
        deny (:obj:`int`): permission bit set
    """

    def __init__(self, id=None, type=None, allow=None, deny=None):
        self.id = id
        self.type = type
        self.allow = allow
        self.deny = deny


class ChannelTypes(Enum):
    GUILD_TEXT = 0
    DM = 1
    GUILD_VOICE = 2
    GROUP_DM = 3
    GUILD_CATEGORY = 4


class Channel(DiscordObject):
    """Represents a guild or DM channel within Discord.

    .. versionadded:: 0.2.0

    Attributes:
        id: the id of this channel
        type: the value_type of channel
        guild_id: the id of the guild
        position: sorting position of the channel
        permission_overwrites: explicit permission overwrites for members and roles
        name : the name of the channel (2-100 characters)
        topic the channel topic (0-1024 characters)
        nsfw: if the channel is nsfw
        last_message_id: the id of the last message sent in this channel (may not point to an existing or valid message)
        bitrate: the bitrate (in bits) of the voice channel
        user_limit: the user limit of the voice channel
        recipients: the recipients of the DM
        icon: icon hash
        owner_id: id of the DM creator
        application_id application id of the group DM creator if it is bot-created
        parent_id: id of the parent category for a channel
        last_pin_timestamp: timestamp when the last pinned message was pinned
    """

    def __init__(self, id: int = None, type: int = ChannelTypes.GUILD_TEXT.value,
                 guild_id: int = None, position: int = None, permission_overwrites: List[Overwrite] = [],
                 name: str = None, topic: str = None, nsfw: bool = False, last_message_id: int = None,
                 bitrate: int = None, user_limit: int = None, recipients: List[User] = [], icon: str = None,
                 owner_id: int = None, application_id: int = None, parent_id: int = None,
                 last_pin_timestamp: int = None):
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

    async def send_message(self, msg: str, tts=False):
        """
        .. versionadded:: 0.3.0
        :param msg: The message to send. If it's over 2000 chars it will be splitted.
        :param tts: Wether to send it as a tts message.

        TODO: Add embed and files.
        """
        if len(msg) <= 2000:
            await self.bot.http.request_url(f'/channels/{self.id}/messages', type='POST',
                                            data={
                                                'content': msg,
                                                'tts': tts
                                            })
        else:
            for x in range(len(msg) // 2000 + 1):
                await self.bot.http.request_url(f'/channels/{self.id}/messages', type='POST',
                                                data={
                                                    'content': msg[x * 2000:x * 2000 + 2000],
                                                    'tts': tts
                                                })

    async def typing(self):
        """Start typing.

        .. versionadded:: 0.3.0
        """
        await self.bot.http.request_url(f'/channels/{self.id}/typing', type='POST')

    async def delete(self):
        """Deletes the channel.

        .. versionadded:: 0.3.0
        """
        await self.bot.http.request_url(f'/channels/{self.id}', type='DELETE')

    def mention(self) -> str:
        """Returns formatted channel mention.

        .. versionadded:: 0.3.0
        """
        return f'<#{self.id}>'

    async def get_messages(self, limit: int = None, around: int = None, before: int = None,
                           after: int = None) -> List['ChannelMessage']:
        """Gets channel messages

        .. versionadded:: 0.3.0
        """

        params = dict()

        if limit is not None and 100 >= limit >= 1:
            params['limit'] = limit
        if around is not None:
            params['around'] = around
        elif before is not None:
            params['before'] = before
        elif after is not None:
            params['after'] = after

        res = await self.bot.http.request_url(f'/channels/{self.id}/messages', params=params)
        return await ChannelMessage.from_api_res(res, self.bot)

    async def get_message(self, message_id) -> 'ChannelMessage':
        """Gets a specific channel message.

        .. versionadded: 0.3.0
        """
        res = await self.bot.http.request_url(f'/channels/{self.id}/messages/{message_id}')
        return await ChannelMessage.from_api_res(res, self.bot)

    async def update(self) -> 'Channel':
        """Updates the channel using the current channel instance properties.

        .. versionadded:: 0.3.0

        :returns: The updated channel.
        """

        data = dict()

        if self.id is None:
            raise AttributeError('The channel must have atleast a id.')
        if self.position is not None:
            data['position'] = self.position
        if self.permission_overwrites is not None:
            data['permission_overwrites'] = self.permission_overwrites
        if self.name is not None:
            data['name'] = self.name
        if self.topic is not None:
            data['topic'] = self.topic
        if self.nsfw is not None:
            data['nsfw'] = self.nsfw
        if self.bitrate is not None:
            data['bitrate'] = self.bitrate
        if self.user_limit is not None:
            data['user_limit'] = self.user_limit
        if self.parent_id is not None:
            data['parent_id'] = self.parent_id

        res = await self.bot.http.request_url(f'/channels/{self.id}', type='PATCH', data=data)
        return await Channel.from_api_res(res, self.bot)

    async def refresh(self) -> 'Channel':
        """Returns a "refreshed" channel instance, may be used to
        make sure you have the latest state of the channel.

        .. versionadded:: 0.3.0

        Example:
            `channel = await channel.refresh()`

        :returns: The requested channel.
        """
        res = await self.bot.http.request_url(f'/channels/{self.id}')
        return await Channel.from_api_res(res, self.bot)

    async def bulk_delete_messages(self, ids: List):
        """Delete multiple messages in a single request.
        This endpoint can only be used on guild channels and requires the MANAGE_MESSAGES permission.

        This endpoint will not delete messages older than 2 weeks,
        and will fail if any message provided is older than that.

        .. versionadded:: 0.3.0
        """
        if not isinstance(ids, list):
            raise TypeError("ids must be a list of id.")
        if not (2 <= len(ids) <= 100):
            raise ValueError("ID list length must be between 2-100")

        data = {
            "messages": ids
        }
        await self.bot.http.request_url(f'/channels/{self.id}/messages/bulk-delete', type='POST', data=data)

    async def get_invites(self) -> List[Invite]:
        """Returns a list of invite objects (with invite metadata) for the channel. Only usable for guild channels.
        Requires the MANAGE_CHANNELS permission.

        .. versionadded:: 0.3.0
        """
        res = await self.bot.http.request_url(f'/channels/{self.id}/invites')
        return await Invite.from_api_res(res, self.bot)

    async def create_invite(self, max_age: int, max_uses=0, temporary=False, unique=False) -> Invite:
        """Create a new invite object for the channel. Only usable for guild channels.
        Requires the CREATE_INSTANT_INVITE permission.

        .. versionadded:: 0.3.0
        """
        res = await self.bot.http.request_url(f'/channels/{self.id}/invites', type='POST', data={
            "max_age": max_age,
            "max_uses": max_uses,
            "temporary": temporary,
            "unique": unique
        })
        return await Invite.from_api_res(res, self.bot)

    async def delete_permission(self, overwrite_id):
        """Delete a channel permission overwrite for a user or role in a channel.
        Only usable for guild channels. Requires the MANAGE_ROLES permission.

        .. versionadded:: 0.3.0
        """
        await self.bot.http.request_url(f'/channels/{self.id}/permissions/{overwrite_id}', type='DELETE')

    async def get_pinned_messages(self) -> List['ChannelMessage']:
        """Returns all pinned messages in the channel as an array of message objects.

        .. versionadded:: 0.3.0
        """
        res = await self.bot.http.request_url(f'/channels/{self.id}/pins')
        return await ChannelMessage.from_api_res(res, self.bot)

    async def pin_message(self, message_id):
        """Pin a message in a channel. Requires the MANAGE_MESSAGES permission.

        .. versionadded:: 0.3.0
        """
        await self.bot.http.request_url(f'/channels/{self.id}/pins/{message_id}', type='PUT')

    async def delete_pinned_message(self, message_id):
        """Delete a pinned message. Requires the MANAGE_MESSAGES permission.

        .. versionadded:: 0.3.0
        """
        await self.bot.http.request_url(f'/channels/{self.id}/pins/{message_id}', type='DELETE')

    async def _from_api_ext(self, key, value):
        if key == 'recipients':
            setattr(self, key, [await User.from_api_res(x, self.bot) for x in value])
        elif key == 'permission_overwrites':
            setattr(self, key, [await Overwrite.from_api_res(x, self.bot) for x in value])
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
        type: type of message activity
        party_id: party_id from a Rich Presence event
    """

    def __init__(self, type: int = None, party_id: int = None):
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

    def __init__(self, id=None, cover_image=None, description=None, icon=None, name=None):
        self.id = id
        self.cover_image = cover_image
        self.description = description
        self.icon = icon
        self.name = name


class Reaction(DiscordObject):
    """Represents a Reaction.

    .. versionadded:: 0.2.0

    Attributes:
        count: times this emoji has been used to react
        me: whether the current user reacted using this emoji
        emoji emoji information
    """

    def __init__(self, count: int = None, me: bool = False, emoji: Emoji = None):
        self.count = count
        self.me = me
        self.emoji = emoji

    async def _from_api_ext(self, key, value):
        if key == 'emoji':
            setattr(self, key, await Emoji.from_api_res(value, self.bot))
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

    def __init__(self, url=None, proxy_url=None, height=None, width=None):
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

    def __init__(self, url=None, height=None, width=None):
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

    def __init__(self, url=None, proxy_url=None, height=None, width=None):
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

    def __init__(self, name=None, url=None):
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

    def __init__(self, name=None, url=None, icon_url=None, proxy_icon_url=None):
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

    def __init__(self, text=None, icon_url=None, proxy_icon_url=None):
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

    def __init__(self, name=None, value=None, inline=False):
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

    def __init__(self, title=None, type=None, description=None, url=None, timestamp=None,
                 color=None, footer=EmbedFooter(), image=EmbedImage(), thumbnail=EmbedThumbnail(),
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
            setattr(self, key, await EmbedFooter.from_api_res(value, self.bot))
        elif key == 'image':
            setattr(self, key, await EmbedImage.from_api_res(value, self.bot))
        elif key == 'thumbnail':
            setattr(self, key, await EmbedThumbnail.from_api_res(value, self.bot))
        elif key == 'video':
            setattr(self, key, await EmbedVideo.from_api_res(value, self.bot))
        elif key == 'provider':
            setattr(self, key, await EmbedProvider.from_api_res(value, self.bot))
        elif key == 'author':
            setattr(self, key, await EmbedAuthor.from_api_res(value, self.bot))
        elif key == 'fields':
            setattr(self, key, [await EmbedField.from_api_res(x, self.bot) for x in value])
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

    def __init__(self, id=None, filename=None, size=None, url=None, proxy_url=None,
                 height=None, width=None):
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
        The author object follows the structure of the :class:`.User` object, but is only a valid user in the case
        where the message is generated by a user or bot user.
        If the message is generated by a :class:`.Webhook`,
        the author object corresponds to the webhook's id, username, and avatar.
        You can tell if a message is generated by a webhook by checking for the webhook_id on the message object.

    Attributes:
        id: id of the message
        channel_id: id of the channel the message was sent in
        author: the author of this message (not guaranteed to be a valid user, see below)
        content: contents of the message
        timestamp: timestamp when this message was sent
        edited_timestamp: timestamp when this message was edited (or null if never)
        tts: whether this was a TTS message
        mention_everyone: whether this message mentions everyone
        mentions: objects users specifically mentioned in the message
        mention_roles: object ids roles specifically mentioned in this message
        attachments: objects any attached files
        embeds: objects any embedded content
        reactions: objects reactions to the message
        nonce: used for validating a message was sent
        pinned whether this message is pinned
        webhook_id: if the message is generated by a webhook, this is the webhook's id
        type: type of message
        activity: activity object sent with Rich Presence-related chat embeds
        application: application object sent with Rich Presence-related chat embeds
    """

    def __init__(self, id=None, channel_id=None, author: User = None, content: str = None, timestamp: int = None,
                 edited_timestamp: int = None, tts: bool = False, mention_everyone: bool = False,
                 mentions: List[User] = [], mention_roles: List[Role] = [], attachments: List[Attachment] = [],
                 embeds: List[Embed] = [], reactions: List[Reaction] = [], nonce: int = None,
                 pinned=False, webhook_id=None, type=None,
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

    async def delete_own_reaction(self, emoji_id):
        """Delete a reaction the bot has made for the message"""
        await self.delete_user_reaction('@me', emoji_id)

    async def delete_user_reaction(self, user_id, emoji_id):
        """Deletes another user's reaction. This endpoint requires the 'MANAGE_MESSAGES'
        permission to be present on the current user.

        .. versionadded: 0.3.0
        """
        await self.bot.http.request_url(f'/channels/{self.channel_id}/messages/{self.id}/'
                                        f'reactions/{emoji_id}/{user_id}', type='DELETE')

    async def delete_all_reactions(self):
        """Deletes all reactions on a message. This endpoint requires the 'MANAGE_MESSAGES'
        permission to be present on the current user.

        .. versionadded: 0.3.0
        """
        await self.bot.http.request_url(f'/channels/{self.channel_id}/messages/{self.id}/reactions', type='DELETE')

    async def get_reactions(self, emoji_id, before: int = None, after: int = None, limit: int = None) -> List[User]:
        """Get a list of users that reacted with this emoji.

        .. versionadded: 0.3.0
        """
        params = dict()

        if before is not None:
            params["before"] = before
        if after is not None:
            params["after"] = after
        if limit is not None:
            if limit > 100:
                limit = 100
            elif limit < 1:
                limit = 1
            params["before"] = limit

        res = await self.bot.http.request_url(f'/channels/{self.channel_id}/messages/{self.id}/'
                                              f'reactions/{emoji_id}', params=params)
        return await User.from_api_res(res, self.bot)

    async def update(self) -> 'ChannelMessage':
        """Updates a previously sent message with the current instance properties (content).
        You can only edit messages that have been sent by the current user. Returns a message object.
        Fires a Message Update Gateway event.

        .. versionadded: 0.3.0

        TODO: Add embed support
        """
        data = dict()
        data["content"] = self.content
        res = await self.bot.http.request_url(f'/channels/{self.channel_id}/messages/{self.id}', type='PATCH',
                                              data=data)
        return await ChannelMessage.from_api_res(res, self.bot)

    async def delete(self):
        """Delete a message.
        If operating on a guild channel and trying to delete a message that was not sent by the current user,
        this endpoint requires the MANAGE_MESSAGES permission

        .. versionadded: 0.3.0
        """
        await self.bot.http.request_url(f'/channels/{self.channel_id}/messages/{self.id}', type='DELETE')

    async def _from_api_ext(self, key, value):
        if key == 'author':
            setattr(self, key, await User.from_api_res(value, self.bot))
        elif key == 'mentions':
            setattr(self, key, [await User.from_api_res(x, self.bot) for x in value])
        elif key == 'mention_roles':
            setattr(self, key, [await Role.from_api_res(x, self.bot) for x in value])
        elif key == 'attachments':
            setattr(self, key, [await Attachment.from_api_res(x, self.bot) for x in value])
        elif key == 'reactions':
            setattr(self, key, [await Reaction.from_api_res(x, self.bot) for x in value])
        elif key == 'activity':
            setattr(self, key, await MessageActivity.from_api_res(value, self.bot))
        elif key == 'activity':
            setattr(self, key, await MessageApplication.from_api_res(value, self.bot))
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
