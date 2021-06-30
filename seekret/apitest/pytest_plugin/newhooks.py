"""
This module contains the hooks specifications to hooks added by the Seekret plugin.
"""

from seekret.apitest.context import Context


def pytest_seekret_context_initialized(context: Context):
    """
    Called when a run profile is loaded.
    Can be used to register auth methods that rely on information from the run profile.
    """
