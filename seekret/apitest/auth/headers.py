from seekret.apitest.auth.base import AuthMethod


class HeadersAuth(AuthMethod):
    IDENTIFIER = 'header'

    def add_headers(self):
        return self.auth_data
