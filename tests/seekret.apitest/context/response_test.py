import io
import json as _json
from typing import Optional, Union

import pytest
from requests import Response
from requests.structures import CaseInsensitiveDict

from seekret.apitest.context.response import ResponseWrapper, NullResultError


def make_wrapper(json=None,
                 headers: Optional[Union[dict[str],
                                         CaseInsensitiveDict[str]]] = None):
    response = Response()
    response.raw = io.BytesIO(_json.dumps(json).encode() if json else b'')
    if headers:
        response.headers = CaseInsensitiveDict(headers)
    return ResponseWrapper(response)


def test_search_json_nested_value():
    wrapper = make_wrapper({'a': {'b': {'c': 'd'}}})
    assert {'c': 'd'} == wrapper.search('json.a.b')


def test_search_json_array_value():
    wrapper = make_wrapper([1, 'b', {'c': 'd'}])
    assert 'd' == wrapper.search('json[2].c')


def test_search_json_missing_value_causes_null_result_error():
    wrapper = make_wrapper({'some-key': 1})
    pytest.raises(NullResultError, wrapper.search, 'json."other-key"')


def test_search_json_value_none_causes_null_result_error():
    wrapper = make_wrapper({'key': None})
    pytest.raises(NullResultError, wrapper.search, 'json.key')


def test_search_json_case_sensitive():
    wrapper = make_wrapper({'caseSensitiveKey': 1})
    pytest.raises(NullResultError, wrapper.search, 'json.casesensitivekey')


def test_search_headers_existing_key():
    wrapper = make_wrapper(headers={'Some-Header': 'value'})
    assert wrapper.search('headers."Some-Header"') == 'value'


def test_search_headers_case_insensitive():
    wrapper = make_wrapper(headers={'Some-Header': 'value'})
    assert wrapper.search('headers."some-header"') == 'value'


def test_search_headers_missing_key_causes_null_result_error():
    wrapper = make_wrapper(headers={'Some-Header': 'value'})
    pytest.raises(NullResultError, wrapper.search, 'headers."other-header"')


def test_search_bad_locator_causes_null_result_error():
    wrapper = make_wrapper(json={'a': 1}, headers={'b': 2})
    pytest.raises(NullResultError, wrapper.search,
                  'expression.must.start.with.json.or.headers')


def test_assert_schema_validation_success():
    wrapper = make_wrapper({
        'a': 'hello!',
        'b': 1,
    })
    wrapper.assert_schema("""
        type: map
        mapping:
            a:
                type: str
                required: true
            b:
                type: int
    """)


def test_assert_schema_validation_failure_causes_assertion_error():
    wrapper = make_wrapper({
        'b': 1,
    })
    pytest.raises(
        AssertionError, wrapper.assert_schema, """
        type: map
        mapping:
            a:
                type: str
                required: true
            b:
                type: int
    """)
