from _pytest.config.argparsing import Parser


def pytest_addoption(parser: Parser, pluginmanager):
    """
    Adds command line options used by the Seekret plugin.
    """

    _ = pluginmanager  # Unused.

    group = parser.getgroup('seekret')
    group.addoption('--run-profile',
                    dest='run_profile',
                    type=str,
                    default=None,
                    help='Run profile YAML file to use for the test session')
