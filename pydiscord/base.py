import json


class DiscordObject:
    """Base class for discord objects."""

    @classmethod
    def from_json(cls, text: str):
        obj = cls()
        json_text = json.loads(text)
        for key, value in json_text.items():
            setattr(obj, key, value)
        return obj
