#!/usr/bin/env python

import sys
import os
import ssl

if sys.version_info[0] < 3:
    import BaseHTTPServer
    Server = BaseHTTPServer
else:
    import http.server
    Server = http.server


class WebRequestHandler(Server.BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200, "No payment required")
        self.send_header('x-powered-by', 'PHP')
        self.send_header('x-request-user-agent', self.headers.get(
            'user-agent', '(unknown)'))
        self.end_headers()

    def do_DELETE(self):
        self.send_response(200, "OK")
        self.end_headers()
        self.wfile.write(self.requestline.encode())

    def do_PATCH(self):
        self.send_response(200, "Patch request ok")
        self.end_headers()
        self.wfile.write(b"Got a patch request")

    def do_GET(self):
        if self.path == '/200':
            self.send_response(200, "OK")
            self.end_headers()
            self.wfile.write(b"Everything is ok!")
        elif self.path == '/200_with_location_header':
            self.send_response(200, "OK")
            self.send_header('Location', '/200')
            self.end_headers()
        elif self.path == '/301_no_location_header':
            self.send_response(301, "Redirect with no location header, hehe")
            self.end_headers()
        elif self.path == '/302':
            self.send_response(302, "Redirect")
            self.send_header('Location', '/200')
            self.end_headers()
        elif self.path == '/304':
            if 'If-Modified-Since' in self.headers:
                self.send_response(304, "Not Modified")
            else:
                self.send_response(200, "Modified")
            self.send_header('Last-Modified', 'February')
            self.end_headers()
        elif self.path == '/404':
            self.send_response(404, "Not Found")
            self.end_headers()
        elif self.path == '/418':
            self.send_response(418, "I'm a teapot")
            self.end_headers()
        elif self.path == '/503':
            self.send_response(503, "Some error")
            self.end_headers()
        elif self.path == '/sesame':
            auth_val = "Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ=="
            if sys.version_info[0] > 2:
                auth_val = "Basic b'QWxhZGRpbjpvcGVuIHNlc2FtZQ=='"
            if 'Authorization' in self.headers and self.headers['Authorization'] == auth_val:
                self.send_response(200, "Sesame open!")
                self.end_headers()
                self.wfile.write(b"Welcome to sesame street!")
            else:
                self.send_response(401, "Sesame closed!")
                self.send_header(
                    'WWW-Authenticate', 'Basic realm="Secure Area"')
                self.end_headers()
        elif self.path == '/hostname':
            self.send_response(200, 'OK')
            self.end_headers()
            host = "***" + self.headers['Host'] + "***"
            self.wfile.write(host.encode())
        elif self.path == '/duplicate_header':
            self.send_response(200, 'OK')
            self.send_header('Duplicate', 'Yes')
            self.send_header('Duplicate', 'Si!')
            self.end_headers()
        elif self.path == '/set_cookie':
            self.send_response(200, 'OK')
            self.send_header('Set-Cookie', 'cookie_monster=happy')
            # self.wfile.write(b"The cookie has been set.")
            self.end_headers()
        elif self.path == '/verify_cookie':
            self.send_response(200, 'OK')
            self.end_headers()
            self.wfile.write(b"<h1>Cookie verification page</h1>")
            if 'cookie_monster=happy' in self.headers.get("Cookie", ""):
                self.wfile.write(b"Cookie Monster is happy.")
            else:
                self.wfile.write(b"Cookie Monster is sad.")
        else:
            self.send_error(500)

    def do_POST(self, *args, **kwargs):
        if self.path == '/echo':
            data = self.rfile.read(int(self.headers['Content-Length']))
            self.rfile.close()
            self.send_response(200, "OK")
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(data)
        elif self.path == '/content_type':
            self.send_response(200, "OK")
            # self.wfile.write(self.rfile.read)
            self.end_headers()
            content_type = self.headers['Content-Type']
            self.wfile.write(content_type.encode())
        elif self.path == '/kill':
            global server
            self.send_response(201, "Killing myself")
            server.socket.close()
            sys.exit(0)
        else:
            self.send_error(500)

    do_PUT = do_POST

PORT = int(sys.argv[1])
server = Server.HTTPServer(('localhost', PORT), WebRequestHandler)
scheme = 'http'

# generate rfhttplibmockserver.pem with the following command:
# openssl req -new -x509 -keyout rfhttplibmockserver.pem -out rfhttplibmockserver.pem -days 365 -nodes
if '--ssl' in sys.argv:
    scheme = 'https'

    cert = os.path.abspath(
        os.path.join(os.path.dirname(__file__), 'rfhttplibmockserver.pem'))

    server.socket = ssl.wrap_socket(server.socket,
                                    certfile=cert,
                                    server_side=True)

print('Starting server on %s://localhost:%d/' % (scheme, PORT))

try:
    server.serve_forever()
except Exception as e:
    print("Server terminated/interrupted with reason: ", e)
