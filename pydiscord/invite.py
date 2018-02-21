from .base import DiscordObject


class Invite(DiscordObject):
    """Represents a code that when used, adds a user to a guild."""

    def __init__(self, code="", guild=None, channel=None):
        self.code = code
        self.guild = guild
        self.channel = channel


class InviteMetadata(DiscordObject):
    def __init__(self, inviter=None, uses=0, max_uses=0, max_age=0, temporary=False,
                 created_at=None, revoked=False):
        self.inviter = inviter
        self.uses = uses
        self.max_uses = max_uses
        self.max_age = max_age
        self.temporary = temporary
        self.created_at = created_at
        self.revoked = revoked
