import livetest

class HTTP:

    # internal

    def __init__(self):
        self._app = None
        self._response = None

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
        self._app = livetest.TestApp(host)


    # request

    def GET(self, url):
        self._response = self.app.get(url)

    def POST(self, url):
        self._response = self.app.post(url)

    def follow_response(self):
        self._response = self.response.follow()

    # status code

    def response_should_succeed(self):
        assert int(self.response.status[0:3]) < 400, \
               'Response should have been success, but was "%s"' % self.response.status

    def response_should_not_succeed(self):
        assert int(self.response.status[0:3]) > 399, \
               'Response should have been success, but was "%s"' % self.response.status

    def response_status_code_should_equal(self, code):
        assert self.response.status.startswith(code), \
               '"%s" does not start with "%s"' % (self.response.status, code)

    def response_status_code_should_not_equal(self, code):
        assert not self.response.status.startswith(code), \
               '"%s" does start with "%s", but should not' % (self.response.status, code)

    # headers

    def response_should_have_header(self, header_name):
        assert header_name in self.response.headers,\
               'Response did not have "%s" header, but should have' % header_name

    def response_should_not_have_header(self, header_name):
        assert not header_name in self.response.headers,\
               'Response did have "%s" header, but should not have' % header_name

    def get_response_header(self, header_name):
        self.response_should_have_header(header_name)
        return self.response.headers[header_name]

    def response_header_should_equal(self, header_name, expected):
        self.response_should_have_header(header_name)
        actual = self.response.headers[header_name]
        assert actual == expected,\
               'Response header "%s" should have been "%s" but was "%s"' % (
                    header_name, expected, actual)

    # debug

    def show_response_in_browser(self, url):
        self._response.showbrowser()
