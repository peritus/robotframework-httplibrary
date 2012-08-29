# based on http://code.activestate.com/recipes/442473-simple-http-server-supporting-ssl-secure-communica/

import socket
from SocketServer import BaseServer
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from OpenSSL import SSL

class SecureHTTPServer(HTTPServer):
    def __init__(self, server_address, HandlerClass, pem_file):
        BaseServer.__init__(self, server_address, HandlerClass)
        ctx = SSL.Context(SSL.SSLv23_METHOD)
        ctx.use_privatekey_file(pem_file)
        ctx.use_certificate_file(pem_file)
        self.socket = SSL.Connection(ctx, socket.socket(self.address_family,
                                                        self.socket_type))
        self.server_bind()
        self.server_activate()

    def shutdown_request(self,request): 
        request.shutdown()

class BaseSecureHTTPRequestHandler(BaseHTTPRequestHandler):
    def setup(self):
        self.connection = self.request
        self.rfile = socket._fileobject(self.request, "rb", self.rbufsize)
        self.wfile = socket._fileobject(self.request, "wb", self.wbufsize)


