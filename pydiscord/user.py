
class UserConnection:
    def __init__(self,
                 id,
                 name,
                 _type,
                 revoked,
                 integrations):
        self.id = id
        self.name = name
        self._type = _type
        self.revoked = revoked
        self.integrations = integrations


class User:
    """Represents a Discord User object"""
    def __init__(self, id, username, discriminator, avatar, bot=False, mfa_enabled=False, verified=False, email=''):
        """The User class constructor
        
        Args:
            id (int): The user's id
            username (str): The user's username, not unique across the platform
            discriminator (str): The user's 4-digit discord-tag
            avatar (str): The user's avatar hash
            bot (bool, optional): Defaults to False. Whether the user belongs to an OAuth2 application
            mfa_enabled (bool, optional): Defaults to False. Whether the user has two factor enabled on their account
            verified (bool, optional): Defaults to False. Whether the email on this account has been verified
        """

        self.id = int(id)
        self.username = username
        self.discriminator = discriminator
        self.avatar = avatar
        self.bot = bot
        self.mfa_enabled = mfa_enabled
        self.verified = verified
        self.email = email

    def __str__(self):
        return "{0}#{1}".format(self.username, self.discriminator)
