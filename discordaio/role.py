from .base import DiscordObject


class Role(DiscordObject):
    """Represents a discord role

    .. versionadded:: 0.2.0

    Attributes:
        id (:obj:`int`): role id
        name (:obj:`str`): role name
        color (:obj:`int`): integer representation of hexadecimal color code
        hoist (:obj:`bool`): if this role is pinned in the user listing
        position (:obj:`int`): position of this role
        permissions (:obj:`int`): permission bit set
        managed (:obj:`bool`): whether this role is managed by an integration
        mentionable (:obj:`bool`): whether this role is mentionable
    """

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


__all__ = [
    'Role',
]
