import unittest.mock as mock

import pytest

from seekret.apitest.context.session import resolve_path_params, Session
from seekret.apitest.runprofile import RunProfile, User, UserAuth


class TestResolvePathParams:
    def test_placeholders_replaced(self):
        assert resolve_path_params(
            '/api/users/{user_name}/channels/{channel_id}', {
                'user_name': 'my-user',
                'channel_id': 'abcd1234'
            }) == '/api/users/my-user/channels/abcd1234'

    def test_invalid_character_escaped(self):
        assert resolve_path_params(
            '/{user_name}',
            {'user_name': 'user/with/slash'}) == '/user%2Fwith%2Fslash'

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
        assert resolve_path_params(
            'api/users/{user_name}/channels/{channel_id}', {
                'user_name': 'my-user',
                'channel_id': 'abcd1234'
            }) == 'api/users/my-user/channels/abcd1234'

    def test_unmatched_placeholders_cause_value_error(self):
        pytest.raises(ValueError, resolve_path_params,
                      'api/users/{user_name}/channels/{channel_id}',
                      {'user_name': 'my-user'})

    def test_unmatched_dict_keys_cause_value_error(self):
        pytest.raises(
            ValueError, resolve_path_params,
            'api/users/{user_name}/channels/{channel_id}', {
                'user_name': 'my-user',
                'channel_id': 'abcd1234',
                'excessive_value': 'not-in-path'
            })


class TestSession:
    class TestPrepareRequest:
        @pytest.fixture
        def mock_request_ctor(self):
            with mock.patch('requests.Request', autospec=True) as m:
                yield m

        @pytest.fixture
        def session(self) -> Session:
            return Session(RunProfile(
                target_server='https://seekret.com',
                users={}
            ))

        def test_path_and_method_only(self, session, mock_request_ctor):
            session._prepare_request(method='GET', path='/my/api')

            assert mock_request_ctor.call_count == 1
            assert mock_request_ctor.call_args == mock.call(
                method='GET',
                url='https://seekret.com/my/api',
                headers=None,
                json=None,
                params=None,
                cookies=None,
                auth=None
            )

        def test_invalid_method(self, session):
            result = session._prepare_request(method='INVALID', path='/my/api')
            assert result.method == 'INVALID'

        def test_path_starts_with_double_slash_normalized_to_single_slash(self, session, mock_request_ctor):
            session._prepare_request(method='GET', path='//my/api')

            assert mock_request_ctor.call_count == 1
            assert mock_request_ctor.call_args == mock.call(
                method='GET',
                url='https://seekret.com/my/api',
                headers=None,
                json=None,
                params=None,
                cookies=None,
                auth=None
            )

        def test_all_values_but_user_given(self, session, mock_request_ctor):
            session._prepare_request(method='GET', path='/my/api/{param}',
                                     json={'data': 'json_value'},
                                     query={'query': 'query_value'},
                                     path_params={'param': 'param_value'},
                                     headers={'header': 'header_value'},
                                     cookies={'cookie': 'cookie_value'})

            assert mock_request_ctor.call_count == 1
            assert mock_request_ctor.call_args == mock.call(
                method='GET',
                url='https://seekret.com/my/api/param_value',
                headers={'header': 'header_value'},
                json={'data': 'json_value'},
                params={'query': 'query_value'},
                cookies={'cookie': 'cookie_value'},
                auth=None
            )

        def test_user_does_not_exist_in_run_profile_causes_key_error(self, session, mock_request_ctor):
            pytest.raises(KeyError, session._prepare_request, method='GET', path='/my/api', user='no-such-user')
            assert not mock_request_ctor.called

        def test_user_exists(self, session):
            session.run_profile.users['test'] = User(auth=UserAuth(
                type='header',
                data={
                    'My-Header': 'apikey'
                }
            ))

            result = session._prepare_request(method='GET', path='/my/api', user='test')
            assert result.headers['My-Header'] == 'apikey'

        def test_user_cached(self, session, mock_request_ctor):
            session.run_profile.users['test'] = User(auth=UserAuth(
                type='test',
                data={}
            ))

            with mock.patch('seekret.apitest.context.session.create_auth', autospec=True) as create_auth_mock:
                session._prepare_request(method='GET', path='/my/api/1', user='test')
                session._prepare_request(method='GET', path='/my/api/2', user='test')

                assert create_auth_mock.call_count == 1
                assert mock_request_ctor.call_count == 2
                assert (mock_request_ctor.call_args_list[0].kwargs['auth'] is
                        mock_request_ctor.call_args_list[1].kwargs['auth'])
