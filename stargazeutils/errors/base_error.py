


class BaseError(Exception):
    def __init__(self, message, cause: Exception = None):
        self.message = message
        self.cause = cause
