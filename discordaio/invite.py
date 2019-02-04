import discordaio
from .base import DiscordObject


class Invite(DiscordObject):
    """Represents a code that when used, adds a user to a guild.

    .. versionadded:: 0.2.0
    """

    def __init__(self, code="", guild: 'discordaio.Guild' = None, channel: 'discordaio.Channel' = None,
                 inviter: 'discordaio.User' = None, uses=0, max_uses=0, max_age=0, temporary=False,
                 created_at=None, revoked=False):
        self.code = code
        self.guild = guild
        self.channel = channel
        self.inviter = inviter
        self.uses = uses
        self.max_uses = max_uses
        self.max_age = max_age
        self.temporary = temporary
        self.created_at = created_at
        self.revoked = revoked

    async def _from_api_ext(self, key, value):
        if key == 'guild':
            setattr(self, key, await discordaio.Guild.from_api_res(value))
        elif key == 'channel':
            setattr(self, key, await discordaio.Channel.from_api_res(value))
        elif key == 'inviter':
            setattr(self, key, await discordaio.User.from_api_res(value))
        else:
            return await super()._from_api_ext(key, value)


__all__ = [
    'Invite'
]
