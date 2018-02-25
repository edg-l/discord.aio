from typing import Optional
from .base import DiscordObject


class VoiceState(DiscordObject):
    """Used to represent a user's voice connection status.
    
    Attributes:
        guild_id (:obj:`int`, optional):
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
