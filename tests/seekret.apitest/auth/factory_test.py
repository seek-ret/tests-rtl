import pytest

import seekret.apitest.auth.factory


@pytest.fixture(autouse=True)
def _patch_methods(monkeypatch):
    monkeypatch.setattr(seekret.apitest.auth.factory,
                        '_SUPPORTED_AUTH_METHODS', {})


def test_register_and_call_factory():
    test_auth_data = {'hi!': 'hey!'}
    test_auth_type_name = 'my-auth-method'
    test_auth_method_sentinel = ''

    @seekret.apitest.auth_method_factory(type_name=test_auth_type_name)
    def my_auth_method(data):
        assert data == test_auth_data
        return test_auth_method_sentinel

    assert seekret.apitest.auth.create_auth(
        test_auth_type_name, test_auth_data) is test_auth_method_sentinel


def test_register_factory_with_existing_name_causes_runtime_error():
    seekret.apitest.auth.factory._SUPPORTED_AUTH_METHODS['existing'] = None
    pytest.raises(RuntimeError,
                  seekret.apitest.register_auth_method_factory,
                  None,
                  type_name='existing')


def test_create_unsupported_type_causes_value_error():
    pytest.raises(ValueError, seekret.apitest.auth.create_auth,
                  'does-not-exist', {})
