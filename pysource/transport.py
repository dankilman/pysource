# Copyright 2014 Dan Kilman
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import json
import socket
from SocketServer import (ThreadingUnixStreamServer,
                          StreamRequestHandler)

from pysource import env
from pysource import ExecutionError
from pysource import remote_call_handlers


RESPONSE_STATUS_OK = "ok"
RESPONSE_STATUS_ERROR = "error"


def _handle(req_type, payload):
    handler = remote_call_handlers.get(req_type)
    if handler is None:
        raise RuntimeError('Unknown request type: {0}'.format(req_type))
    return handler(**payload)


class RequestHandler(StreamRequestHandler):

    def handle(self):
        req = self.rfile
        res = self.wfile
        try:
            req_body_len = int(req.readline())
            req_body = json.loads(req.read(req_body_len))
            req_type = req_body['type']
            req_payload = req_body['payload']
            res_payload = _handle(req_type, req_payload)
            res_status = RESPONSE_STATUS_OK
        except Exception, e:
            res_status = RESPONSE_STATUS_ERROR
            res_payload = {
                'error': str(e)
            }
        res_body = json.dumps({
            'payload': res_payload,
            'status': res_status
        })
        res_body_len = len(res_body)
        res.write(res_body_len)
        res.write('\r\n')
        res.write(res_body)


def do_client_request(req_type, payload):
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(env.unix_socket_path)
    req = sock.makefile('wb', 0)
    res = sock.makefile('rb', -1)
    try:
        req_body = json.dumps({
            'type': req_type,
            'payload': payload
        })
        req_body_len = len(req_body)
        req.write(req_body_len)
        req.write('\r\n')
        req.write(req_body)

        res_body_len = int(res.readline())
        res_body = json.loads(res.read(res_body_len))
        res_body_payload = res_body['payload']
        if res_body['status'] == RESPONSE_STATUS_ERROR:
            error = res_body_payload['error']
            raise ExecutionError('execution failed: {0}'.format(error))
        return res_body_payload
    finally:
        req.close()
        res.close()
        sock.close()


def start_server():
    server = ThreadingUnixStreamServer(env.unix_socket_path,
                                       RequestHandler)
    server.serve_forever()
