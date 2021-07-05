from functools import partial
from typing import Any

_SUPPORTED_AUTH_METHODS = {}


def auth_method_factory(factory=None, *, type_name):
    """
    Register the decorated function as a auth method factory for the given type name.
    The factory will be called by `create_auth` when the type matches the registered type.

    >>> @auth_method_factory(type_name='my-auth')
    >>> def my_auth(data: dict[str, Any]):
    >>>     ...

    :param factory: Decorated factory function.
    :param type_name: Type of the auth method.
    """

    if factory is None:
        return partial(auth_method_factory, type_name=type_name)

    register_auth_method_factory(factory, type_name)
    return factory


def register_auth_method_factory(factory, type_name):
    """
    Register the given function as a auth method factory for the given type name.

    :param factory: Factory function.
    :param type_name: Type of the auth method.
    """

    if type_name in _SUPPORTED_AUTH_METHODS:
        raise RuntimeError(
            f'auth method factory for type "{type_name}" already registered')

    _SUPPORTED_AUTH_METHODS[type_name] = factory


def create_auth(auth_type: str, auth_data: dict[str, Any]):
    """
    Create an auth handler from the given type and data.
    The resulting value can be used as the `auth` parameter in `requests.request` calls.

    :param auth_type: Type of auth handler to create.
    :param auth_data: Data to pass to the auth handler.
    :return: Auth handler available for use in `requests.request` calls.
    """

    try:
        method = _SUPPORTED_AUTH_METHODS[auth_type]
    except KeyError as e:
        raise ValueError(f'unsupported auth type "{auth_type}"') from e

    return method(auth_data)
