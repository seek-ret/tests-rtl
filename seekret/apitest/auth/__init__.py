from box import Box, BoxKeyError

from seekret.apitest.auth.base import AuthMethod
from seekret.apitest.auth.bearer import BearerAuth
from seekret.apitest.auth.custom_request import CustomRequestAuth
from seekret.apitest.auth.headers import HeadersAuth
from seekret.apitest.auth.saveutil import save_authorization

AUTH_METHODS: dict[str, AuthMethod] = {
    method.IDENTIFIER: method()
    for method in AuthMethod.__subclasses__() if method.IDENTIFIER is not None
}


def auth_method_from_info(auth_type: str) -> AuthMethod:
    """
    Create an auth method instance using the auth type and data.

    :param auth_type: Type identifier of the authorization method.
    """

    try:
        return AUTH_METHODS[auth_type]
    except KeyError:
        raise RuntimeError(f'invalid auth type {auth_type}')


def call_on_test_start(test_data: Box, variables: Box, auth_type: str,
                       auth_data: Box):
    auth_method = auth_method_from_info(auth_type)
    return auth_method.on_test_start(test_data, variables, auth_data)


def add_auth_in_headers(runtime_data: Box) -> Box:
    try:
        return runtime_data.auth.headers
    except BoxKeyError:
        return Box()
