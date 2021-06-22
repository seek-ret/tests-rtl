from abc import ABC, abstractmethod

from box import Box


class AuthMethod(ABC):
    """
    Base class for defining authorization methods.

    Subclasses are automatically registered as auth methods and can be requested using `auth.type = IDENTIFIER`.
    """
    IDENTIFIER = None

    @abstractmethod
    def on_test_start(self, test_data: Box, variables: Box, auth_data: Box):
        raise NotImplementedError()
