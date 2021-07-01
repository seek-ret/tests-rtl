import contextlib
import logging
from typing import Any, Optional

from seekret.apitest.context.session import Session

logger = logging.getLogger(__name__)


class Context(object):
    """
    Seekret context and functions.

    This class is the interface from the test function to the Seekret testing infrastructure. It is intended to be used
    as a fixture and returned from the `seekret` fixture.
    """

    def __init__(self, session: Session):
        self.session = session

        self._current_stage_index = 1  # 1-based.

    @contextlib.contextmanager
    def stage(self, method: str, path: str):
        """
        Declare the next test stage targets the given endpoint.

        The purpose of this function is to create a readable structure to tests.

        :param method: Method of the stage target endpoint.
        :param path: Path of the stage target endpoint.
        :return: Callable value for performing requests to the target endpoint.
        """

        logger.info(f'Test Stage #{self._current_stage_index}: {method} {path}')
        try:
            yield _StageWrapper(self, method, path)
        finally:
            self._current_stage_index += 1

    def request(self, *args, user: Optional[str] = 'user', **kwargs):
        return self.session.request(*args, user=user, **kwargs)


class _StageWrapper(object):
    def __init__(self, context: Context, method: str, path: str):
        self._context = context

        self.method = method
        self.path = path

    def __call__(self, json: Optional[Any] = None, **kwargs):
        return self._context.request(self.method,
                                     self.path,
                                     json=json,
                                     **kwargs)
