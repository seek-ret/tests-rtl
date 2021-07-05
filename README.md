# Seekret API testing runtime

The `seekret.apitest` package contains runtime functions and tools intended to ease API testing.

Seekret uses this library in automatically generated tests to help the readability of the generated tests, and implement
common functionalities.

## Quickstart

First, install `seekret.apitest`::

    pip install seekret.apitest

Now, in order to run a test:

1. Store one or more generated tavern tests from the [Seekret website](https://app.seekret.com) in a directory.
2. Copy the configuration file you received from Seekret to the same directory.

Your test directory should look like this:

```text
/testdir
|-- api1_test.py
|-- api2_test.py
|-- ...
|-- run-profile.yaml
```

After you finish setting up your test directory, simply run `pytest`.

### Enable live logging

Use the `--log-cli-level INFO` option to show outgoing requests and incoming responses live as they occur during the
test.

## Run profile

Each test run requires a run profile. By default, Seekret reads the run profile from the `run-profile.yaml` file in the
root directory, but you can provide a different run profile by specifying the `--run-profile` flag.

The run profile sets:

* The target server of the tests
* Users and authentication configurations

```yaml
target_server: https://example.com
users:
  default:
    auth:
      type: bearer
      data:
        token: <API key of the testing account>
```

### Users

The `users` key contains the configuration of the user authentication. The data under the `auth` block describes how to
authenticate as the user.

The following methods are currently available:

* `header` - sends the value in the `data` field as headers.
* `bearer` - sends the value in the `token` field of `data` as a bearer token in the `Authorization` header.

## Example of a generated test

Seekret generates the test to repeat an observed workflow. Values that have no importance to the workflow will be
randomized *during test generation* according to their inferred format.

```python
import seekret.apitest


def test_post_channels_post_messages(seekret: seekret.apitest.Context):
    # Stage 1: POST /api/channels
    with seekret.stage(method='POST', path='/api/channels') as request:
        response = request(json={
            'name': '<random name>'
        })
        assert response.status_code == 201

        carry_0_responseBody_data_channel_id = response.search('json.data.channel.id')

    # Stage 2: POST /api/channels/{channel_id}/messages
    with seekret.stage(method='POST', path='/api/channels/{channel_id}/messages') as request:
        response = request(json={
            'message': '<random message>'
        }, path_params={
            'channel_id': carry_0_responseBody_data_channel_id
        })
        assert response.status_code == 201
```

In this generated tests, there are two stages:

* Create a channel: `POST /api/channels`
* Send a message in the channel: `POST /api/channels/{channel_id}/messages`

Seekret will generate the value transfers between the test stages. For instance, in this case, the ID of the created
channel from the first request, is used as the required `channel_id` path parameter of the second request.

Seekret will also assert that the response has the observed status.

To aid debugging, when a test fails, Seekret will display the data of the requests and responses from the test.

## Deep Dive

The generated test uses the `seekret` fixture, which returns an instance of the `seekret.apitest.Context` class. The
test context allows separating test stages with the `stage` context manager, and sending requests to the target server.
The context uses the information from the [run profile](#run-profile) in order to determine the target server, and the
required authorization data.

You can choose the user for a request with by specifying the `user` parameter in the `request()` call to another user
from the [run profile](#run-profile).

### Setup and teardown

You can add setup and teardown logic to tests
using [pytest fixtures](https://docs.pytest.org/en/stable/fixture.html#fixture). The `seekret` fixture is available for
use in function-scoped fixtures for declaring setup stages and logging.

Consider the following example of setup and teardown logic:

```python
import pytest
import seekret.apitest


@pytest.fixture
def channel(seekret: seekret.apitest.Context):
    # Setup stage: happens before the test.
    with seekret.stage(method='POST', path='/api/channels') as request:
        response = request(json={
            'name': 'Test Channel'
        })
        assert response.status_code == 201

        channel_id = response.search('json.data.channel.id')

    # Yielding runs the actual test body.
    # Important! Yield outside of the stage context. Otherwise the test will start in the context of the setup stage.
    yield channel_id

    # Teardown stage: happens after the test.
    with seekret.stage(method='DELETE', path='/api/channels/{channel_id}'):
        response = request(path_params={
            'channel_id': channel_id
        })
        assert response.status_code == 200


def test_post_messages_delete_messages(seekret: seekret.apitest.Context, channel):
    # The 'channel' parameter has the value yielded from the 'channel' fixture.
    # In this instance, 'channel' will be the ID of the created channel.
    ...
```
