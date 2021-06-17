from box import Box

from seekret.apitest.auth import AuthMethod


class CustomRequestAuth(AuthMethod):
    IDENTIFIER = 'custom-request'

    def on_test_start(self, test_data: Box, variables: Box, auth_data: Box):
        test_data.stages.insert(0, {
            'type': 'ref',
            'id': auth_data.get('auth_stage_id', 'auth')
        })
