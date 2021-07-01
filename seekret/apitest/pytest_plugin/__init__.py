"""
The `seekret.apitest.pytest_plugin` package contains the hooks and fixtures exposed
by the `seekret.apitest` pytest plugin.
"""

from seekret.apitest.pytest_plugin.fixtures import seekret, _seekret_run_profile, seekret_session
from seekret.apitest.pytest_plugin.options import pytest_addoption


def pytest_addhooks(pluginmanager):
    """
    Add hooks supported by the Seekret plugin.
    """
    from seekret.apitest.pytest_plugin import newhooks
    pluginmanager.add_hookspecs(newhooks)


__all__ = [
    'seekret',
    '_seekret_run_profile',  # Required for registering the fixture.
    'seekret_session',
    'pytest_addhooks',
    'pytest_addoption'
]
