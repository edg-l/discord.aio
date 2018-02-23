

class WebSocketCreationError(Exception):
    def __init__(self):
        self.message = "Error creating a websocket to connect to discord."

class EventTypeException(Exception):
    def __init__(self, message):
        self.message = message