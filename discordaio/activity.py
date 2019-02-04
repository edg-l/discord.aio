from .base import DiscordObject


class ActivityParty(DiscordObject):
    """Activity party

    .. versionadded:: 0.2.0

    Attributes:
        id (:obj:`str`, optional): the id of the party
        size (:obj:`list` of :obj:`int`): array of two integers (current_size, max_size), used to show the party's current and maximum size
    """

    def __init__(self, id="", size=[]):
        self.id = id
        self.size = size


class ActivityTimestamps(DiscordObject):
    """Activity timestamps

    .. versionadded:: 0.2.0

    Attributes:
        start (:obj:`int`, optional): unix time (in milliseconds) of when the activity started
        end (:obj:`int`, optional): unix time (in milliseconds) of when the activity ends
    """

    def __init__(self, start=0, end=0):
        self.start = start
        self.end = end


class ActivityAssets(DiscordObject):
    """Activity assets

    .. versionadded:: 0.2.0

    Attributes:
        large_image (:obj:`str`, optional): the id for a large asset of the activity, usually a snowflake
        large_text (:obj:`str`, optional): text displayed when hovering over the large image of the activity
        small_image (:obj:`str`, optional): the id for a small asset of the activity, usually a snowflake
        small_text (:obj:`str`, optional): text displayed when hovering over the small image of the activity
    """

    def __init__(self, large_image="", large_text="", small_image="", small_text=""):
        self.large_image = large_image
        self.large_text = large_text
        self.small_image = small_image
        self.small_text = small_text


class Activity(DiscordObject):
    """Represents a discord activity

    .. versionadded:: 0.2.0

    Attributes:
        name (:obj:`str`): the activity's name
        type (:obj:`int`): activity type
        url (:obj:`str`, optional): stream url, is validated when type is 1
        timestamps (:class:`.Timestamps`): object unix timestamps for start and/or end of the game
        application_id (:obj:`int`, optional): application id for the game
        details (:obj:`str`, optional): what the player is currently doing
        state (:obj:`str`, optional): the user's current party status
        party (:class:`.Party`): object information for the current party of the player
        assets (:class:`.Assets`): object images for the presence and their hover texts
    """

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
            setattr(self, key, await ActivityTimestamps.from_api_res(value, self.bot))
        elif key == 'party':
            setattr(self, key, await ActivityParty.from_api_res(value, self.bot))
        elif key == 'assets':
            setattr(self, key, await ActivityAssets.from_api_res(value, self.bot))
        else:
            await super()._from_api_ext(key, value)


__all__ = [
    'Activity',
    'ActivityParty',
    'ActivityTimestamps',
    'ActivityAssets',
]
