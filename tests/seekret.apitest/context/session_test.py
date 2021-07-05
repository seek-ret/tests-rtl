import pytest

from seekret.apitest.context.session import resolve_path_params


class TestResolvePathParams:
    def test_placeholders_replaced(self):
        assert resolve_path_params('/api/users/{user_name}/channels/{channel_id}', {
            'user_name': 'my-user',
            'channel_id': 'abcd1234'
        }) == '/api/users/my-user/channels/abcd1234'

    def test_invalid_character_escaped(self):
        assert resolve_path_params('/{user_name}', {
            'user_name': 'user/with/slash'
        }) == '/user%2Fwith%2Fslash'

    def test_duplicate_placeholders_replaced_to_same_value(self):
        assert resolve_path_params('/{p0}/{p1}/{p0}', {
            'p0': '0',
            'p1': '1'
        }) == '/0/1/0'

    def test_non_string_params_converted_to_string(self):
        class Custom:
            def __str__(self):
                return 'test'

        assert resolve_path_params('/{string}/{int}/{custom-obj}', {
            'string': 'string',
            'int': 15,
            'custom-obj': Custom()
        }) == '/string/15/test'

    def test_first_char_other_than_slash_is_ok(self):
        assert resolve_path_params('api/users/{user_name}/channels/{channel_id}', {
            'user_name': 'my-user',
            'channel_id': 'abcd1234'
        }) == 'api/users/my-user/channels/abcd1234'

    def test_unmatched_placeholders_cause_value_error(self):
        pytest.raises(ValueError, resolve_path_params, 'api/users/{user_name}/channels/{channel_id}', {
            'user_name': 'my-user'
        })

    def test_unmatched_dict_keys_cause_value_error(self):
        pytest.raises(ValueError, resolve_path_params, 'api/users/{user_name}/channels/{channel_id}', {
            'user_name': 'my-user',
            'channel_id': 'abcd1234',
            'excessive_value': 'not-in-path'
        })
