from typing import Any

from requests import PreparedRequest
from requests.auth import AuthBase

from seekret.apitest.auth.factory import auth_method_factory


@auth_method_factory(type_name='header')
class HeadersAuth(AuthBase):
    def __init__(self, data: dict[str, Any]):
        self.headers = data

    def __call__(self, request: PreparedRequest) -> PreparedRequest:
        request.headers.update(self.headers)
        return request
