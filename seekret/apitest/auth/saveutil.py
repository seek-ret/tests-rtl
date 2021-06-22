from collections.abc import Callable
from enum import Enum
from typing import Any, Optional

import requests
from tavern.util.dict_util import recurse_access_key


class AuthType(Enum):
    HEADER = 'header'
    BEARER = 'bearer'


def _save_auth_header(value, name='Authorization'):
    return {'seekret-runtime': {'v1': {'auth': {'headers': {name: value}}}}}


def _save_header(value, data: dict):
    return _save_auth_header(value,
                             name=data.get('target_header', 'Authorization'))


def _save_bearer(value, _data):
    return _save_auth_header(f'Bearer {value}')


_HANDLERS: dict[AuthType, Callable[[Any, dict], dict]] = {
    AuthType.HEADER: _save_header,
    AuthType.BEARER: _save_bearer,
}


def save_authorization(response: requests.Response,
                       *,
                       type: AuthType,
                       data: Optional[Any] = None,
                       json: Optional[str] = None,
                       headers: Optional[str] = None):
    """
    Tavern extension function for authentication requests that saves authorization tokens for later requests.

    :param response: The response to save values of.
    :param type: Type of authorization method to save the authorization tokens according to.
    :param data: Additional data required for the authorization method.
    :param json: Where in the response JSON content the token appears (mutually exclusive with the "headers" parameter).
    :param headers: Where in the response headers the token appears (mutually exclusive with the "json" parameter).

    Example - use bearer token from body::

        # ...
        save:
            $ext:
                function: seekret.apitest:save_authorization
                extra_kwargs:
                    type: bearer
                    json: data.token  # JMES path to the token.
    """

    has_json = json is not None
    if (headers and has_json) or (not headers and not has_json):
        raise ValueError(
            '"seekret.apitest:save_authorization" requires either a "json" field or a "headers" field'
        )

    if json:
        value = recurse_access_key(response.json(), json)
    else:
        assert headers is not None
        value = recurse_access_key(response.headers, headers)

    try:
        handler = _HANDLERS[AuthType(type)]
    except (KeyError, ValueError):
        raise ValueError(
            f'invalid auth type {type!r} for "seekret.apitest:save_authorization"'
        )

    return handler(value, data)
