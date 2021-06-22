from box import Box

from seekret.apitest.auth.base import AuthMethod


class HeadersAuth(AuthMethod):
    IDENTIFIER = 'header'

    def on_test_start(self, test_data: Box, variables: Box, auth_data: Box):
        variables.merge_update(
            {'seekret-runtime': {
                'v1': {
                    'auth': {
                        'headers': auth_data
                    }
                }
            }})
