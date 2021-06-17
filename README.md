# Seekret API testing runtime

The `seekret.apitest` package contains runtime functions and tools intended to ease API testing.

The `seekret.apitest` package is not used directly, but is referenced within tavern tests generated by Seekret.

## Quickstart

First, install tavern and seekret.apitest: `pip install tavern seekret.apitest`

Now, in order to run a test:

1. Store one or more generated tavern tests from the [Seekret website](https://app.seekret.com) in a directory.
2. Copy the configuration file you received from Seekret to the same directory.

Your test directory should look like this:

```text
/testdir
|-- test_1.tavern.yaml
|-- test_2.tavern.yaml
|-- ...
|-- config.yaml
```

After your test directory is set up, run `pytest --tavern-global-cfg config.yaml`.

Tavern will collect all `test_*.tavern.yaml` files and run the described tests.

## Understanding the configuration and generated tests

Tavern tests generated by Seekret use common variables which are expected to be set using an external configuration.
This currently includes the host of the target servers and the authorization settings.

Example generated test file:

```yaml
# test_1.tavern.yaml

stages:
  - name: POST /user
    request:
      headers:
        $ext:
          function: seekret.apitest:add_auth_in_headers
          # This section defines that the headers are extended with
          # the result of the `add_auth_in_headers` function.
          # The `add_auth_in_headers` function uses Seekret-format
          # authorization settings defined in the configuration file
          # in the "user" variable.
          extra_args:
            - !force_format_include "{seekret-runtime.v1}"
      json:
        # Randomized body values, created during test generation.
        email: jenkinsjennifer@king.com
        name: vrdyin
        photo: https://hernandez.biz/
      method: POST
      url: '{host}/user' # The "host" variable from the configuration file.
    response:
      save:
        json:
          # Later tests can use the `userId` value from this response
          # by specifying this variable name.
          saved_0_responseBody_userId: userId
      status_code:
        - 200
```

Example configuration file:

```yaml
name: Global test configuration
description: |
  Global configuration for running the tavern tests.

variables:
  seekret:
    v1:
      target_server: http://example.com
      users:
        user:
          auth:
            type: bearer
            data:
              token: <Preconfigured API token for the test user>
```

## Adding authentication using a custom request

To extend the authentication capabilities, Seekret allows adding an authentication stage to the test in the
configuration file.

Here's an example of a configuration file that uses custom request authentication:

```yaml
# ...
variables:
  seekret:
    v1:
      # ...
      users:
        user:
          auth:
            type: custom-request
            data:
              auth_stage_id: my-custom-auth-stage # Optional, defaults to "auth"

stages:
  - id: my-custom-auth-stage
    name: My custom auth stage
    request:
    # ...
    response:
      save:
        $ext:
          # Saving using this extension function allows us to save values into nested objects.
          function: seekret.apitest:dots_save
          extra_kwargs:
            headers:
              # This will take the X-Auth-Token header from the response and put it in the header
              # of future test stages.
              seekret-runtime.v1.auth.headers.X-Auth-Token: '"X-Auth-Token"'
```

Before running a tavern test, the Seekret library will prepend the custom authentication stage to the test, so it
executes prior to the test stages defined in the test file.

The stage is in your full control, but you must save the authorization values using the `seekret.apitest:dots_save`
extension function. The `dots_save` extension function allows saving response values into nested objects.

Save values intended for use in request headers in `seekret-runtime.v1.auth.header.<Header Name>`, and values intended
for use in request bodies in `seekret-runtime.v1.auth.json.<path-in-body>`.

The values form `seekret-runtime.v1.auth` are read in every following stage and added to each request.
