from robot.output import LOGGER

from base64 import b64encode
from functools import wraps
from urlparse import urlparse

import livetest
import json
import jsonpointer

def load_json(json_string):
    try:
        return json.loads(json_string)
    except ValueError, e:
        raise ValueError("Could not parse '%s' as JSON: %s" % (json_string, e))

def _with_json(f):
    @wraps(f)
    def wrapper(self, json_string, *args, **kwargs):
        return json.dumps(
          f(self, load_json(json_string), *args, **kwargs))
    return wrapper

class HTTP:
    """
    HttpLibrary for Robot Framework

    *JSON*

    The JSON related keywords use JSON Pointer. To learn more about JSON
    Pointer, go to http://tools.ietf.org/html/draft-pbryan-zyp-json-pointer-00.
    """

    # internal

    def __init__(self):
        self._app = None
        self._response = None
        self._reset()

    def _reset(self):
        self._request_headers = {}
        self._request_body = None

    @property
    def app(self):
        if not self._app:
            raise Exception('Not connected to any HTTP Host. Use "Set HTTP Host" keyword first.')
        return self._app

    @property
    def response(self):
        if not self._response:
            raise Exception('No request available, use e.g. GET to create one.')
        return self._response

    def _path_from_url_or_path(self, url_or_path):

        if url_or_path.startswith("/"):
            return url_or_path

        elif url_or_path.startswith("http"):
            parsed_url = urlparse(url_or_path)
            self.set_http_host(parsed_url.netloc)
            return parsed_url.path

        raise Exception('"%s" needs to be in form of "/path" or "http://host/path"'
                % url_or_path)

    # setup

    def set_http_host(self, host):
        """
        Sets the HTTP host to use for future requests. You must call this
        before issuing any HTTP requests.

        `host` is the name of the host, optionally with port (e.g. 'google.com' or 'localhost:5984')
        """
        self._app = livetest.TestApp(host)

    # request

    def http_request(self, verb, url):
        """
        Issues a HTTP request with an uncommon HTTP Verb.

        `verb` is the HTTP Verb to use, e.g. "PROPFIND", "PATCH", "OPTIONS"
        `url` is the URL relative to the server root, e.g. '/_utils/config.html'
        """
        path = self._path_from_url_or_path(url)

        self._response = self._app.request(path, {}, self._request_headers,
                method=verb.upper(),)
        self._reset()

    def HEAD(self, url):
        """
        Issues a HTTP HEAD request.

        `url` is the URL relative to the server root, e.g. '/_utils/config.html'
        """
        path = self._path_from_url_or_path(url)
        self._response = self.app.head(path, {}, self._request_headers)
        self._reset()

    def GET(self, url):
        """
        Issues a HTTP GET request.

        `url` is the URL relative to the server root, e.g. '/_utils/config.html'
        """
        path = self._path_from_url_or_path(url)
        self._response = self.app.get(path, {}, self._request_headers)
        self._reset()

    def POST(self, url):
        """
        Issues a HTTP POST request.

        `url` is the URL relative to the server root, e.g. '/_utils/config.html'
        """
        path = self._path_from_url_or_path(url)
        kwargs = {}
        if 'Content-Type' in self._request_headers:
            kwargs['content_type'] = self._request_headers['Content-Type']
        self._response = self.app.post(path, self._request_body or {}, self._request_headers, **kwargs)
        self._reset()

    def PUT(self, url):
        """
        Issues a HTTP PUT request.

        `url` is the URL relative to the server root, e.g. '/_utils/config.html'
        """
        path = self._path_from_url_or_path(url)
        kwargs = {}
        if 'Content-Type' in self._request_headers:
            kwargs['content_type'] = self._request_headers['Content-Type']
        self._response = self.app.put(path, self._request_body or {}, self._request_headers, **kwargs)
        self._reset()

    def DELETE(self, url):
        """
        Issues a HTTP DELETE request.

        `url` is the URL relative to the server root, e.g. '/_utils/config.html'
        """
        path = self._path_from_url_or_path(url)
        self._response = self.app.delete(path, {}, self._request_headers)
        self._reset()

    def follow_response(self):
        """
        Follows a HTTP redirect if the previous response status code was a 301 or 302.
        """
        self._response = self.response.follow()

    # status code

    def response_should_succeed(self):
        """
        Fails if the response status code of the previous request was >= 400
        """
        assert int(self.response.status[0:3]) < 400, \
               'Response should have succeeded, but was "%s".' % self.response.status

    def response_should_not_succeed(self):
        """
        Fails if the response status code of the previous request was < 400
        """
        assert int(self.response.status[0:3]) > 399, \
               'Response should not have succeeded, but was "%s".' % self.response.status

    def response_status_code_should_equal(self, status_code):
        """
        Fails if the response status code was not the specified one.

        `status_code` the status code to compare against.
        """
        assert self.response.status.startswith(status_code), \
               '"%s" does not start with "%s", but should have.' % (self.response.status, status_code)

    def response_status_code_should_not_equal(self, status_code):
        """
        Fails if the response status code is equal to the one specified.

        `status_code` the status code to compare against.
        """
        assert not self.response.status.startswith(status_code), \
               '"%s" starts with "%s", but should not.' % (self.response.status, status_code)

    # response headers

    def response_should_have_header(self, header_name):
        """
        Fails if the response does not have a header named `header_name`
        """
        assert header_name in self.response.headers,\
               'Response did not have "%s" header, but should have.' % header_name

    def response_should_not_have_header(self, header_name):
        """
        Fails if the response does has a header named `header_name`
        """
        assert not header_name in self.response.headers,\
               'Response did have "%s" header, but should not have.' % header_name

    def get_response_header(self, header_name):
        """
        Get the response header with the name `header_name`
        """
        self.response_should_have_header(header_name)
        return self.response.headers[header_name]

    def response_header_should_equal(self, header_name, expected):
        """
        Fails if the value of response header `header_name` does not equal `expected`
        """
        self.response_should_have_header(header_name)
        actual = self.response.headers[header_name]
        assert actual == expected,\
               'Response header "%s" should have been "%s" but was "%s".' % (
                    header_name, expected, actual)

    def response_header_should_not_equal(self, header_name, not_expected):
        """
        Fails if the value of response header 'header_name' equals 'expected'
        """
        self.response_should_have_header(header_name)
        actual = self.response.headers[header_name]
        assert actual != not_expected,\
               'Response header "%s" was "%s" but should not have been.' % (
                    header_name, actual)

    def log_response_headers(self, log_level='INFO'):
        """
        Logs the response headers, line by line.

        Specify `log_level` (default: "INFO") to set the log level.
        """
        for name, value in self.response.headers.items():
            LOGGER.write("%s: %s" % (name, value), log_level)

    # request headers

    def set_request_header(self, header_name, header_value):
        """
        Sets a request header for the next request.

        `header_name` is the name of the header, e.g. `User-Agent`
        `header_value` is the key of the header, e.g. `RobotFramework HttpLibrary (Mozilla/4.0)`
        """
        LOGGER.write('Set request header "%s" to "%s"' % (header_name, header_value), 'INFO')
        self._request_headers[header_name] = header_value

    def set_basic_auth(self, username, password):
        """
        Set HTTP Basic Auth for next request.

        See http://en.wikipedia.org/wiki/Basic_access_authentication

        `username` is the username to authenticate with, e.g. 'Aladdin'

        `password` is the password to use, e.g. 'open sesame'
        """
        credentials = "%s:%s" % (username, password)
        LOGGER.write('Set basic auth to "%s"' % credentials, 'INFO')
        self.set_request_header("Authorization", "Basic %s" % b64encode(credentials))

    # payload

    def set_request_body(self, body):
        """
        Set the request body for the next HTTP request.

        Example:
        | Set Request Body           | user=Aladdin&password=open%20sesame |
        | POST                       | /login                              |
        | Response Should Succeed  |                                     |
        """
        LOGGER.write('Request body set to "%s".' % body, 'INFO')
        self._request_body = body.encode("utf-8")

    def get_response_body(self):
        """
        Get the response body.

        Example:
        | GET                 | /foo.xml          |                                      |
        | ${body}=            | Get Response Body |                                      |
        | Should Start With   | ${body}           | <?xml version="1.0" encoding="UTF-8" |
        """
        return self.response.body

    def response_body_should_contain(self, should_contain):
        """
        Fails if the response body does not contain `should_contain`

        Example:
        | GET                          | /foo.xml         |
        | Response Body Should Contain | version="1.0"    |
        | Response Body Should Contain | encoding="UTF-8" |
        """
        assert should_contain in self.response.body,\
               '"%s" should have contained "%s", but did not.' % (self.response.body, should_contain)

    def log_response_body(self, log_level='INFO'):
        """
        Logs the response body.

        Specify `log_level` (default: "INFO") to set the log level.
        """
        LOGGER.write(self.response.body, log_level)

    # json

    def should_be_valid_json(self, json_string):
        """
        Attempts to parse `json_string` as JSON. Fails, if `json_string` is invalid JSON.

        Example:
        | Should Be Valid Json | {"foo": "bar"} |
        """
        load_json(json_string)

    @_with_json
    def get_json_value(self, json_string, json_pointer):
        """
        Get the target node of the JSON document `json_string` specified by `json_pointer`.

        Example:
        | ${result}=       | Get Json Value   | {"foo": {"bar": [1,2,3]}} | /foo/bar |
        | Should Be Equal  | ${result}        | [1, 2, 3]                 |          |
        """
        return jsonpointer.resolve_pointer(json_string, json_pointer)

    def json_value_should_equal(self, json_string, json_pointer, expected_value):
        """
        Fails if the value of the target node of the JSON document
        `json_string` specified by JSON Pointer `json_pointer` is not `expected_value`.

        Example:
        | Set Test Variable       | ${doc}  | {"foo": {"bar": [1,2,3]}} |             |
        | Json Value Should Equal | ${doc}  | /foo/bar                  | "[1, 2, 3]" |
        """

        got = self.get_json_value(json_string, json_pointer)

        assert got == expected_value, \
               'JSON value "%s" does not equal "%s", but should have.' % (got, expected_value)


    def json_value_should_not_equal(self, json_string, json_pointer, expected_value):
        """
        Fails if the value of the target node of the JSON document
        `json_string` specified by JSON Pointer `json_pointer` is `expected_value`.

        Example:
        | Set Test Variable           | ${doc}  | {"foo": {"bar": [1,2,3]}} |             |
        | Json Value Should Not Equal | ${doc}  | /foo/bar                  | "[1, 2, 3]" |
        """

        got = self.get_json_value(json_string, json_pointer)

        assert got != expected_value, \
               'JSON value "%s" does not equal "%s", but should have.' % (got, expected_value)


    @_with_json
    def set_json_value(self, json_string, json_pointer, json_value):
        """
        Set the target node of the JSON document `json_string` specified by
        JSON Pointer `json_pointer` to `json_value`.

        Example:
        | ${result}=       | Set Json Value | {"foo": {"bar": [1,2,3]}} | /foo | 12 |
        | Should Be Equal  | ${result}      | {"foo": 12}               |      |    |
        """
        value = load_json(json_value)
        p = jsonpointer.set_pointer(json_string, json_pointer, value)
        return json_string

    @_with_json
    def log_json(self, json_string, log_level='INFO'):
        """
        Logs a pretty printed version of the JSON document `json_string`.
        """
        for line in json.dumps(json_string, indent=2).split('\n'):
            LOGGER.write(line, log_level)

    # debug

    def show_response_body_in_browser(self):
        """
        Opens your default web browser with the last request's response body.

        This is meant for debugging response body's with complex media types.
        """
        self._response.showbrowser()
