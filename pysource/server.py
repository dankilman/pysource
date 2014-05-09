import os
from SocketServer import (ThreadingUnixStreamServer,
                          StreamRequestHandler)

from pysource import env
from pysource import protocol

class RequestHandler(StreamRequestHandler):

    def handle(self):
        req = self.rfile
        res = self.wfile
        req_type = int(req.readline())
        if req_type == protocol.CLIENT_SOURCE_REGISTER_REQUEST:
            _handle_source_register(req, res)


def _handle_source_register(req, res):
    source_content_len = int(req.readline())
    source_content = req.read(source_content_len)
    exec source_content
    res.write(protocol.SERVER_SOURCE_RESPONSE_SUC)


def run():
    server = ThreadingUnixStreamServer(env.unix_socket_path,
                                       RequestHandler)
    server.serve_forever()
