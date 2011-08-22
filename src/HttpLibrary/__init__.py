import livetest

from base64 import b64encode

from robot.output import LOGGER

class HTTP:

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
            raise Exception('Not connected to any HTTP Host. Use "Connect" keyword first.')
        return self._app

    @property
    def response(self):
        if not self._response:
            raise Exception('No request available, use e.g. GET to create one.')
        return self._response

    # setup

    def connect(self, host):
        """
        Sets the HTTP server for future requests. You must invoke this before
        issuing any HTTP requests.

        'host' is the name of the host, optionally with port (e.g. 'google.com' or 'localhost:5984')
        """
        self._app = livetest.TestApp(host)

    # request

    def HEAD(self, url):
        """
        Issues a HTTP HEAD request.

        'url' is the URL relative to the server root, e.g. '/_utils/config.html'
        """
        self._response = self.app.head(url, {}, self._request_headers)
        self._reset()

    def GET(self, url):
        """
        Issues a HTTP GET request.

        'url' is the URL relative to the server root, e.g. '/_utils/config.html'
        """
        self._response = self.app.get(url, {}, self._request_headers)
        self._reset()

    def POST(self, url):
        """
        Issues a HTTP POST request.

        'url' is the URL relative to the server root, e.g. '/_utils/config.html'
        """
        kwargs = {}
        if 'Content-Type' in self._request_headers:
            kwargs['content_type'] = self._request_headers['Content-Type']
        self._response = self.app.post(url, self._request_body or {}, self._request_headers, **kwargs)
        self._reset()

    def PUT(self, url):
        """
        Issues a HTTP PUT request.

        'url' is the URL relative to the server root, e.g. '/_utils/config.html'
        """
        kwargs = {}
        if 'Content-Type' in self._request_headers:
            kwargs['content_type'] = self._request_headers['Content-Type']
        self._response = self.app.put(url, self._request_body or {}, self._request_headers, **kwargs)
        self._reset()

    def DELETE(self, url):
        """
        Issues a HTTP DELETE request.

        'url' is the URL relative to the server root, e.g. '/_utils/config.html'
        """
        self._response = self.app.delete(url, {}, self._request_headers)
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
               'Response should have succeeded, but was "%s"' % self.response.status

    def response_should_not_succeed(self):
        """
        Fails if the response status code of the previous request was < 400
        """
        assert int(self.response.status[0:3]) > 399, \
               'Response should have been success, but was "%s"' % self.response.status

    def response_status_code_should_equal(self, status_code):
        """
        Fails if the response status code was not the specified one.

        'status_code' the status code to compare against.
        """
        assert self.response.status.startswith(status_code), \
               '"%s" does not start with "%s", but should have.' % (self.response.status, status_code)

    def response_status_code_should_not_equal(self, status_code):
        """
        Fails if the response status code is equal to the one specified.

        'status_code' the status code to compare against.
        """
        assert not self.response.status.startswith(status_code), \
               '"%s" starts with "%s", but should not.' % (self.response.status, status_code)

    # response headers

    def response_should_have_header(self, header_name):
        """
        Fails if the response does not have a header named 'header_name'
        """
        assert header_name in self.response.headers,\
               'Response did not have "%s" header, but should have' % header_name

    def response_should_not_have_header(self, header_name):
        """
        Fails if the response does has a header named 'header_name'
        """
        assert not header_name in self.response.headers,\
               'Response did have "%s" header, but should not have' % header_name

    def get_response_header(self, header_name):
        """
        Get the response header with the name 'header_name'
        """
        self.response_should_have_header(header_name)
        return self.response.headers[header_name]

    def response_header_should_equal(self, header_name, expected):
        """
        Fails if the value of response header 'header_name' does not equal 'expected'
        """
        self.response_should_have_header(header_name)
        actual = self.response.headers[header_name]
        assert actual == expected,\
               'Response header "%s" should have been "%s" but was "%s"' % (
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
        for name, value in self.response.headers.items():
            LOGGER.write("%s: %s" % (name, value), log_level)

    # request headers

    def set_request_header(self, header_name, header_value):
        """
        Sets a request header for the next request.

        'header_name' is the name of the header, e.g. 'User-Agent'
        'header_value' is the key of the header, e.g. 'RobotFramework HttpLibrary (Mozilla/4.0)'
        """
        self._request_headers[header_name] = header_value

    def set_basic_auth(self, username, password):
        """
        Set HTTP Basic Auth for next request.

        See <a href="http://en.wikipedia.org/wiki/Basic_access_authentication">Wikipedia on "Basic access authentication"</a>.

        'username' is the username to authenticate with, e.g. 'Aladdin'
        'password' is the password to use, e.g. 'open sesame'
        """
        self.set_request_header("Authorization", "Basic %s" % b64encode("%s:%s" % (username, password)))

    # payload

    def set_request_body(self, body):
        self._request_body = body.encode("utf-8")

    def get_response_body(self):
        return self.response.body

    def response_body_should_contain(self, should_contain):
        assert should_contain in self.response.body,\
               '"%s" should have contained "%s", but did not.' % (self.response.body, should_contain)

    def log_response_body(self, log_level='INFO'):
        LOGGER.write(self.response.body, log_level)

    # debug

    def show_response_body_in_browser(self):
        """
        Opens your default web browser with the last request's response body.

        This is meant for debugging response body's with complex media types.
        """
        self._response.showbrowser()
