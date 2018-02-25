from typing import Optional
from .base import DiscordObject


class VoiceState(DiscordObject):
    """Used to represent a user's voice connection status.
    
    Attributes:
        guild_id (:obj:`int`, optional): the guild id this voice state is for
        channel_id (:obj:`int`): the channel id this user is connected to
        user_id (:obj:`int`): the user id this voice state is for
        session_id (:obj:`str`): the session id for this voice state
        deaf (:obj:`bool`): whether this user is deafened by the server
        mute (:obj:`bool`): whether this user is muted by the server
        self_deaf (:obj:`bool`): whether this user is locally deafened
        self_mute (:obj:`bool`): whether this user is locally muted
        suppress (:obj:`bool`): whether this user is muted by the current user
    """
    def __init__(self, guild_id: Optional[int]=None, channel_id: int=0, user_id: int=0, session_id: str='', deaf=False,
                 mute=False, self_deaf=False, self_mute=False, suppress=False):
        self.guild_id: int = guild_id
        self.channel_id = channel_id
        self.user_id = user_id
        self.session_id = session_id
        self.deaf = deaf
        self.mute = mute
        self.self_deaf = self_deaf
        self.self_mute = self_mute
        self.suppress = suppress


class VoiceRegion(DiscordObject):
    """
    Attributes:
        id (:obj:`str`): unique ID for the region
        name (:obj:`str`): name of the region
        vip (:obj:`bool`): true if this is a vip-only server
        optimal (:obj:`bool`): true for a single server that is closest to the current user's client
        deprecated (:obj:`bool`): whether this is a deprecated voice region (avoid switching to these)
        custom (:obj:`bool`): whether this is a custom voice region (used for events/etc)
    """
    def __init__(self, id="", name="", vip=False, optimal=False, deprecated=False,
                 custom=False):
        self.id = id
        self.name = name
        self.vip = vip
        self.optimal = optimal
        self.deprecated = deprecated
        self.custom = custom


__all__ = [
    'VoiceState',
    'VoiceRegion',
]
