from typing import Type

from box import Box

from seekret.apitest.auth.base import AuthMethod
from seekret.apitest.auth.bearer import BearerAuth
from seekret.apitest.auth.headers import HeadersAuth

AUTH_TYPES: dict[str, Type[AuthMethod]] = {
    method.IDENTIFIER: method for method in AuthMethod.__subclasses__() if method.IDENTIFIER is not None
}


def _auth_method_from_info(auth_type: str, auth_data: Box) -> AuthMethod:
    """
    Create an auth method instance using the auth type and data.

    :param auth_type: Type identifier of the authorization method.
    :param auth_data: Data used by the authorization method.
    """

    try:
        auth_method_type = AUTH_TYPES[auth_type]
    except KeyError:
        raise RuntimeError(f'invalid auth type {auth_type}')

    return auth_method_type(auth_data)


def add_auth_in_headers(*, auth_type: str, auth_data: Box) -> Box:
    auth_method = _auth_method_from_info(auth_type, auth_data)
    return auth_method.add_headers()
