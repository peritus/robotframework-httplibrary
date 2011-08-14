#!/usr/bin/env python

import BaseHTTPServer
from sys import exit

class WebRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/200':
            self.send_response(200, "OK")
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
        elif self.path == '/418':
            self.send_response(418, "I'm a teapot")
        elif self.path == '/503':
            self.send_response(503, "Some error")
        else:
            self.send_error(500)

    def do_POST(self, *args, **kwargs):
        if self.path == '/echo':
            self.send_response(200, "OK")
            self.wfile.write(self.rfile.read)
        elif self.path == '/kill':
            global server
            self.send_response(201, "Killing myself")
            server.socket.close()
            exit(0)
        else:
            self.send_error(500)

server = BaseHTTPServer.HTTPServer(('localhost', 36503), WebRequestHandler)    
server.serve_forever()

print 'Listening on http://localhost:36503/'
