"""
LiveTest - Like WebTest, but on a live site.

Setup an app to test against with just a hostname:

>>> import livetest
>>> app = livetest.TestApp('pypi.python.org')

Make requests just like WebTest:

>>> resp = app.get('/pypi')

Grab forms:

>>> resp.forms # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
{0: <webtest.Form object at 0x...>,
 1: <webtest.Form object at 0x...>,
 u'searchform': <webtest.Form object at 0x...>}
>>> form = resp.forms[0]
>>> form.fields # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
{u'term': [<webtest.Text object at 0x...>],
 u':action': [<webtest.Hidden object at 0x...>],
 u'submit': [<webtest.Submit object at 0x...>]}

Submit forms:

>>> form['term'] = 'python testing'
>>> resp = form.submit()

Test stuff in the response:

>>> resp.mustcontain('livetest', 'Index', 'Package')
>>> resp.status
'200 OK'

"""

__author__ = 'storborg@mit.edu'
__version__ = '0.5'

import sys
import webtest
import httplib
import urlparse
from Cookie import BaseCookie, CookieError

conn_classes = {'http': httplib.HTTPConnection,
                'https': httplib.HTTPSConnection}


class TestApp(webtest.TestApp):
    def _load_conn(self, scheme):
        if scheme in conn_classes:
            self.conn[scheme] = conn_classes[scheme](self.host)
        else:
            raise ValueError("Scheme '%s' is not supported." % scheme)

    def __init__(self, host, scheme='http', relative_to=None):
        self.host = host
        self.relative_to = relative_to
        self.conn = {}
        self._load_conn(scheme)
        self.extra_environ = {
          'wsgi.url_scheme': scheme,
        }
        self.reset()

    def _do_httplib_request(self, req):
        "Convert WebOb Request to httplib request."
        headers = dict((name, val) for name, val in req.headers.iteritems())
        if req.scheme not in self.conn:
            self._load_conn(req.scheme)

        conn = self.conn[req.scheme]
        conn.request(req.method, req.path_qs, req.body, headers)

        webresp = conn.getresponse()
        res = webtest.TestResponse()
        res.status = '%s %s' % (webresp.status, webresp.reason)
        res.body = webresp.read()
        response_headers = []
        for headername in dict(webresp.getheaders()).keys():
            for headervalue in webresp.msg.getheaders(headername):
                response_headers.append((headername, headervalue))
        res.headerlist = response_headers
        res.errors = ''
        return res

    def do_request(self, req, status, expect_errors):
        """
        Override webtest.TestApp's method so that we do real HTTP requests
        instead of WSGI calls.
        """
        headers = {}
        if self.cookies:
            c = BaseCookie()
            for name, value in self.cookies.items():
                c[name] = value
            hc = '; '.join(['='.join([m.key, m.value]) for m in c.values()])
            req.headers['Cookie'] = hc

        res = self._do_httplib_request(req)
        # Set these attributes for consistency with webtest.
        res.request = req
        res.test_app = self

        if not expect_errors:
            self._check_status(res.status_int, res)
            self._check_errors(res)
        res.cookies_set = {}

        for header in res.headers.getall('set-cookie'):
            try:
                c = BaseCookie(header)
            except CookieError, e:
                raise CookieError(
                    "Could not parse cookie header %r: %s" % (header, e))
            for key, morsel in c.items():
                self.cookies[key] = morsel.value
                res.cookies_set[key] = morsel.value
        return res


def goto(self, href, method='get', **args):
    """
    Monkeypatch the TestResponse.goto method so that it doesn't wipe out the
    scheme and host.
    """
    scheme, host, path, query, fragment = urlparse.urlsplit(href)
    # We
    fragment = ''
    href = urlparse.urlunsplit((scheme, host, path, query, fragment))
    href = urlparse.urljoin(self.request.url, href)
    method = method.lower()
    assert method in ('get', 'post'), (
        'Only "get" or "post" are allowed for method (you gave %r)'
        % method)
    if method == 'get':
        method = self.test_app.get
    else:
        method = self.test_app.post
    return method(href, **args)

webtest.TestResponse.goto = goto
