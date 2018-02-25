from .base import DiscordObject
from .guild import Guild
from .channel import Channel
from .user import User


class Invite(DiscordObject):
    """Represents a code that when used, adds a user to a guild.

    .. versionadded:: 0.2.0

    Attributes:
        code (:obj:`str`): the invite code (unique ID)
        guild (:class:`.Guild`): the guild this invite is for
        channel (:class:`.Channel`): the channel this invite is for
    """

    def __init__(self, code="", guild=None, channel=None):
        self.code = code
        self.guild = guild
        self.channel = channel

    async def _from_api_ext(self, key, value):
        if key == 'guild':
            setattr(self, key, await Guild.from_api_res(value))
        elif key == 'channel':
            setattr(self, key, await Channel.from_api_res(value))
        else:
            return await super()._from_api_ext(key, value)


class InviteMetadata(DiscordObject):
    """Represents the invite metadata

    .. versionadded:: 0.2.0

    Attributes:
        inviter (:class:`.A`): user object user who created the invite
        uses (:obj:`int`): number of times this invite has been used
        max_uses (:obj:`int`): max number of times this invite can be used
        max_age (:obj:`int`): duration (in seconds) after which the invite expires
        temporary (:obj:`bool`): whether this invite only grants temporary membership
        created_at (:obj:`int`): timestamp when this invite was created
        revoked (:obj:`bool`): whether this invite is revoked
    """

    def __init__(self, inviter=None, uses=0, max_uses=0, max_age=0, temporary=False,
                 created_at=None, revoked=False):
        self.inviter = inviter
        self.uses = uses
        self.max_uses = max_uses
        self.max_age = max_age
        self.temporary = temporary
        self.created_at = created_at
        self.revoked = revoked

    async def _from_api_ext(self, key, value):
        if key == 'inviter':
            setattr(self, key, await User.from_api_res(value))
        else:
            return await super()._from_api_ext(key, value)


__all__ = [
    'Invite',
    'InviteMetadata',
]
