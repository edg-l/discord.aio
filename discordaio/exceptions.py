import sys


class WebSocketCreationError(Exception):
    def __init__(self):
        print("Error creating a websocket to connect to discord.", file=sys.stderr)


class EventTypeError(Exception):
    pass


class AuthorizationError(Exception):
    def __init__(self, message):
        self.message = message


class BadRequestError(Exception):
    def __init__(self, message):
        self.message = message


class NotFoundError(Exception):
    def __init__(self, message):
        self.message = message


class GatewayUnavailable(Exception):
    def __init__(self, message):
        self.message = message


class UnhandledEndpointStatusError(Exception):
    pass


__all__ = [
    'WebSocketCreationError',
    'EventTypeError',
    'AuthorizationError',
    'UnhandledEndpointStatusError'
]
