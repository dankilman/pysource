import json
from SocketServer import (ThreadingUnixStreamServer,
                          StreamRequestHandler)

from pysource import env
from pysource import protocol
from pysource import request_context


def _handle_source_register(payload):
    exec payload['source_content']
    names = [reg.name for reg in request_context.registered]
    return {'names': names}


def _handle(req_type, payload):
    handler = lambda payload: 'none'
    if req_type == protocol.SOURCE_REGISTER_REQUEST:
        handler = _handle_source_register
    return handler(payload)


class RequestHandler(StreamRequestHandler):

    def handle(self):
        req = self.rfile
        res = self.wfile
        req_body_len = int(req.readline())
        req_body = json.loads(req.read(req_body_len))
        req_type = req_body['type']
        req_payload = req_body['payload']
        res_payload = _handle(req_type, req_payload)
        res_body = json.dumps({'payload': res_payload})
        res_body_len = len(res_body)
        res.write(res_body_len)
        res.write('\r\n')
        res.write(res_body)


def run():
    server = ThreadingUnixStreamServer(env.unix_socket_path,
                                       RequestHandler)
    server.serve_forever()
