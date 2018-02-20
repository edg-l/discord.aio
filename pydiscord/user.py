import json


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

    __slots__ = ['id', 'username', 'discriminator', 'avatar', 'bot', 'mfa_enabled', 'verified', 'email']

    def __init__(self, id=None, username=None, discriminator=None, avatar=None, bot=False, mfa_enabled=False, verified=False, email=False):
        """The User class constructor

        Args:
            id (int, optional): Defaults to None. The user's id
            username (str, optional): Defaults to None. The user's username, not unique across the platform
            discriminator ([str, optional): Defaults to None. The user's 4-digit discord-tag
            avatar ([str, optional): Defaults to None. The user's avatar hash
            bot (bool, optional): Defaults to False. Whether the user belongs to an OAuth2 application
            mfa_enabled (bool, optional): Defaults to False. Whether the user has two factor enabled on their account
            verified (bool, optional): Defaults to False. Whether the email on this account has been verified
            email (str, optional): Defaults to False. The user's email
        """

        self.id = id
        self.username = username
        self.discriminator = discriminator
        self.avatar = avatar
        self.bot = bot
        self.mfa_enabled = mfa_enabled
        self.verified = verified
        self.email = email


    @classmethod
    def from_json(cls, json_text):
        """Creates a ``User`` from a json string.
        
        Args:
            json_text (str): The json string containing the user's information.
        
        Returns:
            User: The user
        """

        user_dict = json.loads(json_text)

        user = User()

        user.id = user_dict['id']
        user.username = user_dict['username']
        user.discriminator = user_dict['discriminator']
        user.avatar = user_dict['avatar']
        user.bot = user_dict['bot']
        user.mfa_enabled = user_dict['mfa_enabled']
        user.verified = user_dict['verified']
        user.email = user_dict['email']

        return user

    def __str__(self):
        return "{0}#{1}".format(self.username, self.discriminator)

    def __repr__(self):
        return "({0}#{1}, {2})".format(self.username, self.discriminator, self.id)
