"""Users in Discord are generally considered the base entity. Users can spawn across the entire platform,
be members of guilds, participate in text and voice chat, and much more. Users are separated by a distinction of "bot" vs "normal." 
Although they are similar, bot users are automated users that are "owned" by another user. Unlike normal users, 
bot users do not have a limitation on the number of Guilds they can be a part of."""

from .base import DiscordObject
from .constants import DISCORD_CDN


class UserConnection(DiscordObject):
    """Represents a discord user connection

    .. versionadded:: 0.2.0

    Attributes:
        id (:obj:`str`): id of the connection account
        name (:obj:`str`): the username of the connection account
        type (:obj:`str`): the service of the connection (twitch, youtube)
        revoked (:obj:`bool`): whether the connection is revoked
        integrations (:obj:`list`): an array of partial server integrations
    """

    def __init__(self, id="", name="", type="", revoked=False, integrations=[]):
        self.id = id
        self.name = name
        self.type = type
        self.revoked = revoked
        self.integrations = integrations


class User(DiscordObject):
    """Represents a discord user

    .. versionadded:: 0.2.0

    Attributes:
        id (:obj:`int`): the user's id identify
        username (:obj:`str`): the user's username, not unique across the platform identify
        discriminator (:obj:`str`): the user's 4-digit discord-tag identify
        avatar (:obj:`str`): the user's avatar hash identify
        bot (:obj:`bool`, optional): whether the user belongs to an OAuth2 application identify
        mfa_enabled (:obj:`bool`, optional): whether the user has two factor enabled on their account identify
        verified (:obj:`bool`, optional): whether the email on this account has been verified email
        email (:obj:`str`, optional): the user's email email
    """

    def __init__(self, id=0, username="", discriminator="", avatar="", bot=False,
                 mfa_enabled=False, verified=False, email=""):
        self.id = id
        self.username = username
        self.discriminator = discriminator
        self.avatar = avatar
        self.bot = bot
        self.mfa_enabled = mfa_enabled
        self.verified = verified
        self.email = email

    def __str__(self):
        return f'{self.username}#{self.discriminator}'

    def __repr__(self):
        return f'<User Object: {self.username}#{self.discriminator}, {self.id}>'

    def get_avatar_url(self):
        return DISCORD_CDN + f'/avatars/{self.id}/{self.avatar}.png'

    def get_default_avatar_url(self):
        return DISCORD_CDN + f'/embed/avatars/{int(self.discriminator) % 5}.png'

    async def _from_api_ext(self, key, value):
        if key == 'guild_id':
            pass
        else:
            await super()._from_api_ext(key, value)


__all__ = [
    'User',
    'UserConnection',
]
