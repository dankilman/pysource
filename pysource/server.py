import os
from SocketServer import (ThreadingUnixStreamServer,
                          BaseRequestHandler)

from pysource import env

class RequestHandler(BaseRequestHandler):

    def handle(self):
        pass


def run():
    server = ThreadingUnixStreamServer(env.unix_socket_path, RequestHandler)
    server.serve_forever()
