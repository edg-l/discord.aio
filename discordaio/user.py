"""Users in Discord are generally considered the base entity. Users can spawn across the entire platform,
be members of guilds, participate in text and voice chat, and much more. Users are separated by a distinction of "bot" vs "normal." 
Although they are similar, bot users are automated users that are "owned" by another user. Unlike normal users, 
bot users do not have a limitation on the number of Guilds they can be a part of."""

from .base import DiscordObject
from .constants import DISCORD_CDN

class UserConnection(DiscordObject):
    """A Discord User Connection"""

    def __init__(self, id="", name="", type="", revoked=False, integrations=[]):
        self.id = id
        self.name = name
        self.type = type
        self.revoked = revoked
        self.integrations = integrations


class User(DiscordObject):
    """A Discord User Object"""

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