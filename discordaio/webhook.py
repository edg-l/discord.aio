"""Webhooks are a low-effort way to post messages to channels in Discord. They do not require a bot user or authentication to use."""

from .base import DiscordObject


class Webhook(DiscordObject):
    """Used to represent a webhook.

    .. versionadded:: 0.2.0

    Attributes:
        id (:obj:`int`): the id of the webhook
        guild_id (:obj:`int`, optional): the guild id this webhook is for
        channel_id (:obj:`int`): the channel id this webhook is for
        user (:class:`.User`): the user this webhook was created by (not returned when getting a webhook with its token)
        name (:obj:`str`): the default name of the webhook
        avatar (:obj:`str`): the default avatar of the webhook
        token (:obj:`str`): the secure token of the webhook
    """

    def __init__(self, id=0, guild_id=0, channel_id=0, user=None, name="",
                 avatar="", token=""):
        self.id = id
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.user = user
        self.name = name
        self.avatar = avatar
        self.token = token


__all__ = [
    'Webhook',
]
