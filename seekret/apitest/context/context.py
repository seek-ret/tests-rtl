import contextlib
from typing import Any, Optional

import requests
from requests.structures import CaseInsensitiveDict

from seekret.apitest.auth import create_auth
from seekret.apitest.context.response import ResponseWrapper
from seekret.apitest.runprofile import RunProfile


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

    :note: Path parameter placeholders that do not appear in the mapping will remain as placeholders.
    :note: Parmaeter names in the mapping that do not appear in the path are ignored.
    """

    if path_params:
        for param_name, value in path_params.items():
            path = path.replace('{' + param_name + '}', value)

    return path


class Context(object):
    """
    Seekret context and functions.

    This class is the interface from the test function to the Seekret testing infrastructure. It is intended to be used
    as a fixture and returned from the `seekret` fixture.
    """
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

    @contextlib.contextmanager
    def stage(self, method: str, path: str):
        """
        Declare the next test stage targets the given endpoint.

        The purpose of this function is to create a readable structure to tests.

        :param method: Method of the stage target endpoint.
        :param path: Path of the stage target endpoint.
        :return: Callable value for performing requests to the target endpoint.
        """

        yield _StageWrapper(self, method, path)

    def request(self,
                method: str,
                path: str,
                json: Optional[Any] = None,
                *,
                path_params: Optional[dict[str, Any]] = None,
                query: Optional[dict[str, Any]] = None,
                headers: Optional[CaseInsensitiveDict[str, Any]] = None,
                cookies: Optional[dict[str, Any]] = None,
                user: Optional[str] = 'user'):
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

        path = resolve_path_params(path, path_params)
        return ResponseWrapper(
            requests.request(method=method,
                             url='/'.join([
                                 self.run_profile.target_server,
                                 path.lstrip('/')
                             ]),
                             headers=headers,
                             json=json,
                             params=query,
                             cookies=cookies,
                             auth=user and self._auth_handler(user)))


class _StageWrapper(object):
    def __init__(self, context: 'Context', method: str, path: str):
        self._context = context

        self.method = method
        self.path = path

    def __call__(self, json: Optional[Any] = None, **kwargs):
        return self._context.request(self.method,
                                     self.path,
                                     json=json,
                                     **kwargs)
