from .base import DiscordObject
from .user import User
from .emoji import Emoji
from .constants import DISCORD_CDN
from .channel import Channel
from .role import Role

import logging
logger = logging.getLogger(__name__)


class GuildEmbed(DiscordObject):
    """Represents a guild embed

    .. versionadded:: 0.2.0

    Attributes:
        enabled (:obj:`bool`): if the embed is enabled
        channel_id (:obj:`int`): the embed channel id
    """

    def __init__(self, enabled=False, channel_id=0):
        self.enabled = enabled
        self.channel_id = channel_id


class GuildMember(DiscordObject):
    """Represents a guild member

    .. versionadded:: 0.2.0

    Attributes:
        user (:class:`.User`): user object
        nick (:obj:`str`, optional): this users guild nickname (if one is set)
        roles (:obj:`list` of :obj:`int`): array of role object ids
        joined_at (:obj:`int`): timestamp when the user joined the guild
        deaf (:obj:`bool`): if the user is deafened
        mute (:obj:`bool`): if the user is muted
    """

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
        elif key == 'guild_id':
            pass
        else:
            await super()._from_api_ext(key, value)

    def __str__(self):
        return self.user.__str__()

    def __repr__(self):
        return f'<GuildMember Object: {self.user.username}#{self.user.discriminator}>'


class Guild(DiscordObject):
    """Represents a guild

    .. versionadded:: 0.2.0

    Note:
        Guilds in Discord represent an isolated collection of users and channels, and are often referred to as "servers" in the UI.

    Attributes:
        id (:obj:`int`): guild id
        name (:obj:`str`): guild name (2-100 characters)
        icon (:obj:`str`): icon hash
        splash (:obj:`str`): splash hash
        owner (:obj:`bool`, optional): whether or not the user is the owner of the guild
        owner_id (:obj:`int`): id of owner
        permissions (:obj:`int`, optional): total permissions for the user in the guild (does not include channel overrides)
        region (:obj:`str`): voice region id for the guild
        afk_channel_id (:obj:`int`): id of afk channel
        afk_timeout (:obj:`int`): afk timeout in seconds
        embed_enabled (:obj:`bool`, optional): is this guild embeddable (e.g. widget)
        embed_channel_id (:obj:`int`, optional): id of embedded channel
        verification_level (:obj:`int`): verification level required for the guild
        default_message_notifications (:obj:`int`): default message notifications level
        explicit_content_filter (:obj:`int`): explicit content filter level
        roles (:obj:`list` of :class:`.Role`): roles in the guild
        emojis (:obj:`list` of :class:`.Emoji`): custom guild emojis
        features (:obj:`list` of :class:`.Strings`): enabled guild features
        mfa_level (:obj:`int`): required MFA level for the guild
        application_id (:obj:`int`): application id of the guild creator if it is bot-created
        widget_enabled (:obj:`bool`, optional): whether or not the server widget is enabled
        widget_channel_id (:obj:`int`, optional): the channel id for the server widget
        system_channel_id (:obj:`int`): the id of the channel to which system messages are sent
        joined_at (:obj:`int`, optional): timestamp when this guild was joined at
        large (:obj:`bool`, optional): whether this is considered a large guild
        unavailable (:obj:`bool`, optional): is this guild unavailable
        member_count (:obj:`int`, optional): total number of members in this guild
        voice_states (:obj:`list` of :class:`.Partial`): (without the guild_id key)
        members (:obj:`list` of :class:`.Guild`): users in the guild
        channels (:obj:`list` of :class:`.Channel`): channels in the guild
        presences (:obj:`list` of :class:`.Partial`): presences of the users in the guild
    """

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

    async def leave(self):
        """Leaves a guild.

        .. versionadded:: 0.3.0
        """
        await self.bot.http.request_url(f'/users/@me/guilds/{self.id}', type='DELETE')

    async def get_member(self, member_id: int) -> GuildMember:
        """Gets a guild member.

        .. versionadded:: 0.3.0

        :param member_id: The member id
        """
        res = await self.bot.http.request_url(f'/guilds/{self.id}/members/{member_id}')
        return await GuildMember.from_api_res(res, self.bot)

    async def get_members(self):
        """Gets and fills the guild with the members info.

        .. versionadded:: 0.3.0
        """
        res = await self.bot.http.request_url(f'/guilds/{self.id}/members')
        self.members = []
        for member in res:
            self.members.append(await GuildMember.from_api_res(member, self.bot))

    async def create_channel(self, channel: Channel) -> Channel:
        """Creates a new guild channel

        .. versionadded:: 0.3.0

        :param channel: The channel to create.
        """
        data = dict()
        if channel.name is None:
            raise ValueError('Channel name must be set when creating a guild channel')
        else:
            data['name'] = channel.name

        if channel.type is not None:
            data['type'] = channel.type

        if channel.bitrate is not None:
            data['bitrate'] = channel.bitrate

        if channel.user_limit is not None:
            data['user_limit'] = channel.user_limit

        if channel.permission_overwrites is not None:
            data['permission_overwrites'] = channel.permission_overwrites

        if channel.parent_id is not None:
            data['parent_id'] = channel.parent_id

        if channel.nsfw is not None:
            data['nsfw'] = channel.nsfw

        res = await self.bot.http.request_url(f'/guilds/{self.id}/channels', type='POST', data=data)
        return await Channel.from_api_res(res, self.bot)

    async def get_channels(self) -> Channel:
        """Returns a list of channels withing the guild.

        .. versionadded:: 0.3.0
        """

        res = await self.bot.http.request_url(f'/guilds/{self.id}/channels')
        return await Channel.from_api_res(res, self.bot)

    async def delete(self) -> None:
        """Deletes the guild

        .. versionadded:: 0.3.0

        Raises:
            AuthorizationError: Raised if you have no authorization to delete the guild.
        """
        return await self.bot.http.request_url(f'/guilds/{self.id}', type='DELETE')

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

    def is_owner(self, member: GuildMember) -> bool:
        """Returns wether the guild member is the owner of the guild

        .. versionadded:: 0.2.0

        Args:
            member (:class:`.GuildMember`): The member

        Returns:
            bool: True if it's the owner, False otherwise.
        """
        return self.owner_id == member.user.id

    def get_icon(self) -> str:
        """Returns the guild icon

        .. versionadded:: 0.2.0

        Returns:
            str: The icon link"""
        return DISCORD_CDN + f'/icons/{self.id}/{self.icon}.png'

    def get_splash(self):
        """Returns the guild splash

        .. versionadded:: 0.2.0

        Returns:
            str: The splash link"""
        return DISCORD_CDN + f'/splashes/{self.id}/{self.splash}.png'

    def __str__(self):
        return f'{self.name}#{self.id}'

    def __repr__(self):
        return f'<Guild Object: {self.name}#{self.id}>'


class IntegrationAccount(DiscordObject):
    """Represents a integration account

    .. versionadded:: 0.2.0

    Attributes:
        id (:obj:`str`): id of the account
        name (:obj:`str`): name of the account
    """

    def __init__(self, id="", name=""):
        self.id = id
        self.name = name


class Integration(DiscordObject):
    """Represents a integration

    .. versionadded:: 0.2.0

    Attributes:
        id (:obj:`int`): integration id
        name (:obj:`str`): integration name
        type (:obj:`str`): integration type (twitch, youtube, etc)
        enabled (:obj:`bool`): is this integration enabled
        syncing (:obj:`bool`): is this integration syncing
        role_id (:obj:`int`): id that this integration uses for "subscribers"
        expire_behavior (:obj:`int`): the behavior of expiring subscribers
        expire_grace_period (:obj:`int`): the grace period before expiring subscribers
        user (:class:`.User`): object user for this integration
        account (:class:`.Account`):  account information
        synced_at (:obj:`int`): timestamp when this integration was last synced
    """

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
    """Represents a ban

    .. versionadded:: 0.2.0

    Attributes:
        reason (:obj:`str`): the reason for the ban
        user (:class:`.User`): the banned user
    """

    def __init__(self, reason="", user=None):
        self.reason = reason
        self.user = user

    async def _from_api_ext(self, key, value):
        if key == 'user':
            setattr(self, key, await User.from_api_res(value))
        else:
            return await super()._from_api_ext(key, value)


__all__ = [
    'Guild',
    'GuildMember',
    'GuildEmbed',
    'IntegrationAccount',
    'Integration',
    'Ban',
]
