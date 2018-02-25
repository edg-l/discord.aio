import json

from .base import DiscordObject
from .user import User
from .constants import DISCORD_CDN


class Emoji(DiscordObject):
    """Represents a emoji object

    .. versionadded:: 0.2.0

    Attributes:
        id (:obj:`int`): emoji id
        name (:obj:`str`): emoji name
        roles (:obj:`list` of :class:`.Role`): object ids roles this emoji is whitelisted to
        user (:class:`.User`): object user that created this emoji
        require_colons (:obj:`bool`, optional): whether this emoji must be wrapped in colons
        managed (:obj:`bool`, optional): whether this emoji is managed
        animated (:obj:`bool`, optional): whether this emoji is animated
    """

    def __init__(self, id=0, name="", roles=[], user=None, require_colons=False,
                 managed=False, animated=False):
        self.id = id
        self.name = name
        self.roles = roles
        self.user = user
        self.require_colons = require_colons
        self.managed = managed
        self.animated = animated

    async def _from_api_ext(self, key, value):
        # Note: roles here is only an array of ids
        if key == 'user':
            setattr(self, key, await User.from_api_res(value))
        else:
            return await super()._from_api_ext(key, value)

    def get_url(self):
        return DISCORD_CDN + f'/emojis/{self.id}.png'


__all__ = [
    'Emoji',
]
