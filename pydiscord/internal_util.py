

def get_class_list(cls, lst: list):
    """Parses a list of classes"""

    from .user import User
    from .guild import GuildMember

    objects = []
    for dct in lst:
        obj = cls()
        for key1, value1 in dct.items():
            if key1 == 'user':
                setattr(obj, key1, User.from_dict(value1))
            elif key1 == 'members':
                get_class_list(GuildMember, value1)
            else:
                setattr(obj, key1, value1)
        objects.append(obj)
    return objects
