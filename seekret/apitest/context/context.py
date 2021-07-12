import contextlib
import logging
from typing import Any, Optional, Union, NewType, cast

from seekret.apitest.context.session import Session

logger = logging.getLogger(__name__)

_NotSet = NewType("_NotSet", object)
NOT_SET = cast(_NotSet, object())

User = Optional[Union[str, _NotSet]]


class Context(object):
    """
    Seekret context and functions.

    This class is the interface from the test function to the Seekret testing infrastructure. It is intended to be used
    as a fixture and returned from the `seekret` and `seekret_module` fixtures.
    """
    def __init__(self, session: Session, scope: str):
        """
        Initialize the context.

        :param session: Seekret session associated with this context.
        :param scope: The scope of this context. The scope is used for logging only, and is
                      specified in the stage start log.
        """
        self.session = session
        self._scope = scope

        self._current_stage_index = 1  # 1-based.
        self.default_user: User = 'default'

    @contextlib.contextmanager
    def stage(self, method: str, path: str):
        """
        Declare the next test stage targets the given endpoint.

        The purpose of this function is to create a readable structure to tests.

        :param method: Method of the stage target endpoint.
        :param path: Path of the stage target endpoint.
        :return: Callable value for performing requests to the target endpoint.
        """

        if self._scope == 'function':
            # Special case: in function scope don't print a prefix at all.
            prefix = ''
        else:
            prefix = self._scope.title() + ' '

        logger.info(
            prefix +
            f'Test Stage #{self._current_stage_index}: {method} {path}')
        try:
            yield _StageWrapper(self, method, path)
        finally:
            self._current_stage_index += 1

    def request(self, *args, user: User = NOT_SET, **kwargs):
        return self.session.request(
            *args,
            user=(self.default_user if user is NOT_SET else user),
            **kwargs)


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
