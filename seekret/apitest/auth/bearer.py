from typing import Any

from requests import PreparedRequest
from requests.auth import AuthBase

from seekret.apitest.auth.factory import auth_method_factory


@auth_method_factory(type_name='bearer')
class BearerAuth(AuthBase):
    def __init__(self, data: dict[str, Any]):
        self.token = data['token']

    def __call__(self, request: PreparedRequest) -> PreparedRequest:
        request.headers['Authorization'] = f'Bearer {self.token}'
        return request
