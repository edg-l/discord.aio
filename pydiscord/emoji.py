import json

from .base import DiscordObject
from .internal_util import get_class_list
from .user import User


class Emoji(DiscordObject):
    def __init__(self, id=0, name="", roles=[], user=None, require_colons=False,
                 managed=False, animated=False):
        self.id = id
        self.name = name
        self.roles = roles
        self.user = user
        self.require_colons = require_colons
        self.managed = managed
        self.animated = animated

    @classmethod
    def from_json(cls, text: str):
        obj = cls()
        json_text = json.loads(text)
        for key, value in json_text.items():
            if key == 'user':
                setattr(obj, key, User.from_dict(value))
            else:
                setattr(obj, key, value)
        return obj