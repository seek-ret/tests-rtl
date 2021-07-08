import io
import json

import jmespath
import pykwalify.core
import requests


class NullResultError(RuntimeError):
    """
    Raised when `response.search` results in a 'null' JSON value, which is the case when a JMESPath
    expression does not find a matching value.
    """
    pass


class ResponseWrapper(object):
    """
    Wrapper for `requests.Response` that extends the response with extra functionality.
    """
    def __init__(self, response: requests.Response):
        """
        Wrap the given response.
        """

        self._response = response

    def __getattr__(self, item):
        return getattr(self._response, item)

    def search(self, expression: str):
        """
        Search the response using the given JMESPath expression.

        >>> response = make_response(json={
        >>>     'keyInBody': 'body-value'
        >>> }, headers={
        >>>     'X-Key-In-Header': 'header-value'
        >>> })
        >>> response.search(response, 'json.keyInBody')  # 'body-value'
        >>> response.search(response, "headers.'X-Key-In-Header'")  # 'header-value'

        :param expression: JMESPath expression pointing to the requested response value.
                           Available root keys are "json" or "headers".
        """

        search_data = {'headers': self.headers}

        try:
            search_data['json'] = self.json()
        except json.JSONDecodeError:
            pass

        value = jmespath.search(expression, search_data)
        if value is None:
            raise NullResultError(
                f'searching response for expression {expression} resulted in null'
            )

        return value

    def assert_schema(self, schema: str):
        """
        Assert that the schema of the response body matches the given PyKwalify schema.

        :param schema: YAML representation of the PyKwalify schema.
        :raises AssertionError: Schema validation failed.
        """
        try:
            pykwalify.core.Core(
                source_data=self.json(),
                schema_file_obj=io.StringIO(schema)).validate()
        except pykwalify.core.SchemaError as e:
            raise AssertionError(
                f'response schema verification error: {e.msg}') from e
