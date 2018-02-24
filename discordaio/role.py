from .base import DiscordObject


class Role(DiscordObject):
    def __init__(self, id=0, name="", color=0, hoist=False, position=0,
                 permissions=0, managed=False, mentionable=False):
        self.id = id
        self.name = name
        self.color = color
        self.hoist = hoist
        self.position = position
        self.permissions = permissions
        self.managed = managed
        self.mentionable = mentionable

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Role Object: {self.name}#{self.id}>'
