from box import Box

from seekret.apitest.auth.base import AuthMethod


class BearerAuth(AuthMethod):
    IDENTIFIER = 'bearer'

    def add_headers(self):
        return Box({'Authorization': f'Bearer {self.auth_data.token}'})
