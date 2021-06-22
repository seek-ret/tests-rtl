from box import Box
from requests import Response

from seekret.apitest.auth import call_on_test_start


def pytest_tavern_beta_before_every_request(request_args: Box):
    """
    Log the outgoing request.

    :note: This is a hook function intended to be imported in a conftest.py file in the tavern test directory.
    """

    print(f'Outgoing request {request_args.method} {request_args.url}')


def pytest_tavern_beta_after_every_response(expected, response: Response):
    """
    Log the incoming response.

    :note: This is a hook function intended to be imported in a conftest.py file in the tavern test directory.
    """

    print(
        f'Incoming response: {response.status_code} {response.reason} from {response.url}'
    )
    print(f'Incoming response: {response.content} from {response.url}')


def pytest_tavern_beta_before_every_test_run(test_dict: dict, variables: dict):
    """
    Allow the auth method to modify the test data and variables.
    """

    test_box = Box(test_dict)
    variables_box = Box(variables)

    auth_type = variables_box.seekret.v1.users.user.auth.type
    auth_data = variables_box.seekret.v1.users.user.auth.data

    call_on_test_start(test_box, variables_box, auth_type, auth_data)

    test_dict.update(test_box.to_dict())
    variables.update(variables_box.to_dict())
