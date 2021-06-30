import io

import jmespath
import pykwalify.core
import requests


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

        return jmespath.search(expression, {
            'json': self.json(),
            'headers': self.headers
        })

    def assert_schema(self, schema):
        try:
            pykwalify.core.Core(
                source_data=self.json(),
                schema_file_obj=io.StringIO(schema)).validate()
        except pykwalify.core.SchemaError as e:
            raise AssertionError(
                f'response schema verification error: {e.msg}') from e
