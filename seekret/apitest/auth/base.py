from abc import ABC

from box import Box


class AuthMethod(ABC):
    """
    Base class for defining authorization methods.

    Subclasses are automatically registered as auth methods and can be requested using `auth.type = IDENTIFIER`.
    """
    IDENTIFIER = None

    def __init__(self, auth_data: Box):
        self.auth_data = auth_data

    def add_headers(self) -> Box:
        return Box()
