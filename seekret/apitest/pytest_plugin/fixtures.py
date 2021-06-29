import pytest

from seekret.apitest.context import Context
from seekret.apitest.context.session import Session
from seekret.apitest.runprofile import RunProfile


@pytest.fixture(scope='session')
def _seekret_run_profile(pytestconfig) -> RunProfile:
    run_profile_path = pytestconfig.getoption(
        'run_profile',
        default=None) or pytestconfig.rootpath / 'run-profile.yaml'
    return RunProfile.load(run_profile_path)


@pytest.fixture(scope='session')
def seekret_session(_seekret_run_profile, pytestconfig) -> Session:
    """
    Seekret test session object.
    """

    session = Session(_seekret_run_profile)
    pytestconfig.hook.pytest_seekret_session_initialized(session=session)
    return session


@pytest.fixture
def seekret(seekret_session, pytestconfig) -> Context:
    """
    Seekret context and functions.
    """

    return Context(session=seekret_session)
