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

    @classmethod
    def from_json_array(cls, text: str):
        objs = []
        json_text = json.loads(text)
        #print(json_text)
        for jobj in json_text:
            c = cls()
            for key, value in jobj.items():
                setattr(c, key, value)
            objs.append(c)
        return objs

    @classmethod
    def from_dict(cls, dct: dict):
        obj = cls()
        for key, value in dct.items():
            setattr(obj, key, value)
        return obj