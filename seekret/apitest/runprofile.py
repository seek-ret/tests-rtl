import dataclasses
from os import PathLike
from typing import Any

import yaml


@dataclasses.dataclass(frozen=True)
class UserAuth(object):
    type: str
    data: dict[str, Any]


@dataclasses.dataclass(frozen=True)
class User(object):
    auth: UserAuth


@dataclasses.dataclass(frozen=True)
class RunProfile(object):
    """
    Configuration values for the a test session.
    """

    target_server: str

    users: dict[str, User]

    @classmethod
    def load(cls, path: PathLike):
        with open(path, 'r') as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)

        return cls(target_server=data['target_server'],
                   users={
                       user_name:
                       User(auth=UserAuth(type=user['auth']['type'],
                                          data=user['auth']['data']))
                       for user_name, user in data['users'].items()
                   })
