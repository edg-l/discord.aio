from .base import DiscordObject


class ActivityParty(DiscordObject):
    def __init__(self, id="", size=[]):
        self.id = id
        self.size = size


class ActivityTimestamps(DiscordObject):
    def __init__(self, start=0, end=0):
        self.start = start
        self.end = end


class ActivityAssets(DiscordObject):
    def __init__(self, large_image="", large_text="", small_image="", small_text=""):
        self.large_image = large_image
        self.large_text = large_text
        self.small_image = small_image
        self.small_text = small_text


class Activity(DiscordObject):
    def __init__(self, name="", type=0, url="", timestamps=None, application_id=0,
                 details="", state="", party=None, assets=None):
        self.name = name
        self.type = type
        self.url = url
        self.timestamps = timestamps
        self.application_id = application_id
        self.details = details
        self.state = state
        self.party = party
        self.assets = assets

    async def _from_api_ext(self, key, value):
        if key == 'timestamps':
            setattr(self, key, await ActivityTimestamps.from_api_res(value))
        elif key == 'party':
            setattr(self, key, await ActivityParty.from_api_res(value))
        elif key == 'assets':
            setattr(self, key, await ActivityAssets.from_api_res(value))
        else:
            await super()._from_api_ext(key, value)
