from box import Box

from seekret.apitest.auth.base import AuthMethod


class BearerAuth(AuthMethod):
    IDENTIFIER = 'bearer'

    def on_test_start(self, test_data: Box, variables: Box, auth_data: Box):
        variables.merge_update({
            'seekret-runtime': {
                'v1': {
                    'auth': {
                        'headers': {
                            'Authorization': f'Bearer {auth_data.token}'
                        }
                    }
                }
            }
        })
