

class WebSocketCreationError(Exception):
    def __init__(self):
        self.message = "Error creating a websocket to connect to discord."
