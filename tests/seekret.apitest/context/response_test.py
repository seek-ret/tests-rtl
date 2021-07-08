import io
import json as _json
from typing import Optional, Union

import pytest
from requests import Response
from requests.structures import CaseInsensitiveDict

from seekret.apitest.context.response import ResponseWrapper


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


def test_search_json_missing_value():
    wrapper = make_wrapper({'some-key': 1})
    assert wrapper.search('json."other-key"') is None


def test_search_json_case_sensitive():
    wrapper = make_wrapper({'caseSensitiveKey': 1})
    assert wrapper.search('json.casesensitivekey') is None


def test_search_headers_existing_key():
    wrapper = make_wrapper(headers={'Some-Header': 'value'})
    assert wrapper.search('headers."Some-Header"') == 'value'


def test_search_headers_case_insensitive():
    wrapper = make_wrapper(headers={'Some-Header': 'value'})
    assert wrapper.search('headers."some-header"') == 'value'


def test_search_headers_missing_key():
    wrapper = make_wrapper(headers={'Some-Header': 'value'})
    assert wrapper.search('headers."other-header"') is None


def test_search_bad_locator():
    wrapper = make_wrapper(json={'a': 1}, headers={'b': 2})
    assert wrapper.search('expression.must.start.with.json.or.headers') is None


def test_assert_schema_validation_succeeds():
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


def test_assert_schema_validation_fails():
    wrapper = make_wrapper({
        'b': 1,
    })
    pytest.raises(
        AssertionError, lambda: wrapper.assert_schema("""
        type: map
        mapping:
            a:
                type: str
                required: true
            b:
                type: int
    """))
