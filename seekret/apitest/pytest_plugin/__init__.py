"""
The `seekret.apitest.pytest_plugin` package contains the hooks and fixtures exposed
by the `seekret.apitest` pytest plugin.
"""
from _pytest.config import Config

from seekret.apitest.pytest_plugin.fixtures import seekret, _seekret_run_profile, seekret_session, seekret_module
from seekret.apitest.pytest_plugin.options import pytest_addoption


def pytest_addhooks(pluginmanager):
    """
    Add hooks supported by the Seekret plugin.
    """
    from seekret.apitest.pytest_plugin import newhooks
    pluginmanager.add_hookspecs(newhooks)


def pytest_configure(config: Config):
    config.addinivalue_line(
        'markers',
        'default_user(user): modify the default user seerket uses for the test'
    )


__all__ = [
    'seekret',
    '_seekret_run_profile',  # Required for registering the fixture.
    'seekret_session',
    'seekret_module',
    'pytest_addhooks',
    'pytest_configure',
    'pytest_addoption'
]
