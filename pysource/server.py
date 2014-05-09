import os
from SocketServer import (ThreadingUnixStreamServer,
                          BaseRequestHandler)

from pysource import env

class RequestHandler(BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024)
        response = "{}: {}".format('oh boy', data)
        self.request.sendall(response)


def run():
    server = ThreadingUnixStreamServer(env.unix_socket_path, RequestHandler)
    server.serve_forever()
