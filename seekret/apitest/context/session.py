import json as _json
import logging
import re
import urllib.parse
from collections.abc import Mapping
from typing import Optional, Any

import requests
from requests.structures import CaseInsensitiveDict

from seekret.apitest.auth import create_auth
from seekret.apitest.context.response import ResponseWrapper
from seekret.apitest.runprofile import RunProfile

PATH_PARAMETER_PLACEHOLDER_PATTERN = re.compile(r'{(?P<param_name>[^{}]+)}')

logger = logging.getLogger(__name__)


def _log_and_print(level: int, message: str):
    logger.log(level, message)
    print(message)


def resolve_path_params(path: str, path_params: dict[str, Any]):
    """
    Resolves path parameters in the path according to the given dictionary.

    >>> resolve_path_params('/api/users/{user_name}/channels/{channel_id}', {
    >>>     'user_name': 'my-user',
    >>>     'channel_id': 'abcd1234'
    >>> })
    >>> # '/api/users/my-user/channels/abcd1234'

    :param path: Path to resolve the path parameters in.
    :param path_params: Dictionary mapping parameter names to their values.

    :raises ValueError: A path parameter placeholder does not have a value in the given dictionary.
    :raises ValueError: Some keys of the given path parameters do not appear as placeholders in the path.
    """

    consumed_params = set()

    def substitute_handler(match: re.Match):
        param_name = match.group('param_name')
        consumed_params.add(param_name)

        # safe defaults to the "/" character, which we need to escape.
        return urllib.parse.quote(str(path_params[param_name]), safe='')

    try:
        resolved = PATH_PARAMETER_PLACEHOLDER_PATTERN.sub(
            substitute_handler, path)
    except KeyError as e:
        raise ValueError(f'expected path param {e} was not given') from e

    unused_params = path_params.keys() - consumed_params
    if unused_params:
        raise ValueError(
            f'path params given but do not appear in path: {", ".join(unused_params)}'
        )

    return resolved


class Session(object):
    def __init__(self, run_profile: RunProfile):
        self.run_profile = run_profile

        self._auths = {}

    def _auth_handler(self, user_name: str):
        """
        Get the auth handler of the requested user.
        """

        try:
            return self._auths[user_name]
        except KeyError:
            user = self.run_profile.users[user_name]
            auth = create_auth(user.auth.type, user.auth.data)
            self._auths[user_name] = auth

            return auth

    def request(self,
                method: str,
                path: str,
                json: Optional[Any] = None,
                *,
                path_params: Optional[dict[str, Any]] = None,
                query: Optional[dict[str, Any]] = None,
                headers: Optional[Mapping[str, Any]] = None,
                cookies: Optional[dict[str, Any]] = None,
                user: Optional[str] = None):
        """
        Perform an HTTP request.

        :param method: The HTTP method of the request.
        :param path: The path in the server to request. Use only the *path* part of the URL.
                     The target server from the run profile is prepended to the value to form the full URL.
        :param json: JSON value to serialize and send in the request body.
        :param path_params: Value of parameters in the path.
        :param query: Query parameters to send in the request.
        :param headers: Headers to send in the request.
        :param cookies: Cookies to send in the request.
        :param user: The requesting user. The available users are defined in the run profile.
                     Use `None` to send an unauthenticated request.
        :return: Wrapped response object.
        """

        prepared_request = self._prepare_request(method,
                                                 path,
                                                 json=json,
                                                 path_params=path_params,
                                                 query=query,
                                                 headers=headers,
                                                 cookies=cookies,
                                                 user=user)

        def _prettify(v):
            if isinstance(v, CaseInsensitiveDict):
                v = dict(v.items())  # Use `v.items()` to preserve case.

            indentation = ' ' * 6  # Match indentation of titles.
            return indentation.join(
                _json.dumps(v, indent=2).splitlines(keepends=True))

        _log_and_print(logging.INFO, f'--> {method} {prepared_request.url}')
        print(f'      headers: {_prettify(prepared_request.headers)}')
        print(f'      json: {_prettify(json)}')

        with requests.Session() as session:
            response = session.send(prepared_request)

        _log_and_print(
            logging.INFO,
            f'<-- {response.status_code} {response.reason} from {method} {response.url}'
        )
        print(f'      headers: {_prettify(response.headers)}')
        try:
            body = _prettify(response.json())
        except ValueError:
            body = response.text
        print(f'      body: {body}')

        return ResponseWrapper(response)

    def _prepare_request(self,
                         method: str,
                         path: str,
                         json: Optional[Any] = None,
                         *,
                         path_params: Optional[dict[str, Any]] = None,
                         query: Optional[dict[str, Any]] = None,
                         headers: Optional[Mapping[str, Any]] = None,
                         cookies: Optional[dict[str, Any]] = None,
                         user: Optional[str] = None):
        path = resolve_path_params(path, path_params or {})
        # Strip "/" at the start of the path to avoid "//" replacing the host part.
        url = urllib.parse.urljoin(self.run_profile.target_server,
                                   path.lstrip('/'))
        return requests.Request(method=method,
                                url=url,
                                headers=headers,
                                json=json,
                                params=query,
                                cookies=cookies,
                                auth=user
                                and self._auth_handler(user)).prepare()
