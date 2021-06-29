import pytest

from seekret.apitest.context import Context
from seekret.apitest.runprofile import RunProfile


@pytest.fixture(scope='session')
def _seekret_run_profile(pytestconfig) -> RunProfile:
    run_profile_path = pytestconfig.getoption(
        'run_profile',
        default=None) or pytestconfig.rootpath / 'run-profile.yaml'
    return RunProfile.load(run_profile_path)


@pytest.fixture(scope='session')
def seekret(_seekret_run_profile, pytestconfig) -> Context:
    """
    Seekret context and functions.
    """

    context = Context(_seekret_run_profile)

    pytestconfig.hook.pytest_seekret_context_initialized(context=context)

    return context
