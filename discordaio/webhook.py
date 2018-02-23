"""Webhooks are a low-effort way to post messages to channels in Discord. They do not require a bot user or authentication to use."""

from .base import DiscordObject


class Webhook(DiscordObject):
    """Used to represent a webhook."""

    def __init__(self, id=0, guild_id=0, channel_id=0, user=None, name="",
                 avatar="", token=""):
        self.id = id
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.user = user
        self.name = name
        self.avatar = avatar
        self.token = token
