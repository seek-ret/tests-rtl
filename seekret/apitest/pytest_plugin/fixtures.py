import pytest
from _pytest.mark import Mark

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


@pytest.fixture(scope='module')
def seekret_module(seekret_session, request) -> Context:
    """
    Seekret test module object.
    """

    return Context(session=seekret_session, scope=request.scope)


@pytest.fixture
def seekret(seekret_session, request) -> Context:
    """
    Seekret context and functions.
    """

    context = Context(session=seekret_session, scope=request.scope)

    default_user: Mark = request.node.get_closest_marker('default_user')
    if default_user is not None:
        context.default_user = default_user.args[0]

    return context
