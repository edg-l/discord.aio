from .base import DiscordObject


class VoiceState(DiscordObject):
    def __init__(self, guild_id=0, channel_id=0, user_id=0, session_id="", deaf=False,
                 mute=False, self_deaf=False, self_mute=False, suppress=False):
        self.guild_id = guild_id
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
