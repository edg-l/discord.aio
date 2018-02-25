import sys


class WebSocketCreationError(Exception):
    def __init__(self):
        print("Error creating a websocket to connect to discord.", file=sys.stderr)


class EventTypeError(Exception):
    pass


class AuthorizationError(Exception):
    def __init__(self):
        print(
            'You requested a api endpoint which you have no authorization', file=sys.stderr)


class UnhandledEndpointStatusError(Exception):
    pass


__all__ = [
    'WebSocketCreationError',
    'EventTypeError',
    'AuthorizationError',
]
