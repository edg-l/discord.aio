
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
    def __init__(self, id, username, discriminator, avatar, is_bot=False, mfa_enabled=False, verified=False, email=''):
        self.id = id
        self.username = username
        self.discriminator = discriminator
        self.avatar = avatar
        self.is_bot = is_bot
        self.mfa_enabled = mfa_enabled
        self.verified = verified
        self.email = email

    def __str__(self):
        return "{0}#{1}".format(self.username, self.discriminator)