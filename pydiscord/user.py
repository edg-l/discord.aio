from .base import DiscordObject


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
        return "{0}#{1}".format(self.username, self.discriminator)

    def __repr__(self):
        return "({0}#{1}, {2})".format(self.username, self.discriminator, self.id)
