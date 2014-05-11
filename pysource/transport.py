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

import os
import json
import socket
from SocketServer import (ThreadingUnixStreamServer,
                          StreamRequestHandler)

from pysource import env
from pysource import ExecutionError
from pysource import remote_call_handlers


RESPONSE_STATUS_OK = "ok"
RESPONSE_STATUS_ERROR = "error"

unix_socket_path = os.path.join(env.pysource_dir, 'socket')


def _handle(req_type, payload):
    handler = remote_call_handlers.get(req_type)
    if handler is None:
        raise RuntimeError('Unknown request type: {0}'.format(req_type))
    return handler(**payload)


class RequestHandler(StreamRequestHandler):

    def handle(self):
        try:
            res_status = RESPONSE_STATUS_OK
            res_payload = _handle(**_read_body(self.rfile))
        except Exception, e:
            res_status = RESPONSE_STATUS_ERROR
            res_payload = {'error': str(e)}
        _write_body(self.wfile, {
            'payload': res_payload,
            'status': res_status
        })


def do_client_request(req_type, payload):
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(unix_socket_path)
    req = sock.makefile('wb', 0)
    res = sock.makefile('rb', -1)
    try:
        _write_body(req, {
            'req_type': req_type,
            'payload': payload
        })
        res_body = _read_body(res)
        res_body_payload = res_body['payload']
        if res_body['status'] == RESPONSE_STATUS_ERROR:
            error = res_body_payload['error']
            raise ExecutionError('execution failed: {0}'.format(error))
        return res_body_payload
    finally:
        req.close()
        res.close()
        sock.close()


def do_piped_client_request(req_type, payload):
    pass


def _read_body(sock):
    json_body_len = int(sock.readline())
    return json.loads(sock.read(json_body_len))


def _write_body(sock, body):
    json_body = json.dumps(body)
    json_body_len = len(json_body)
    sock.write(json_body_len)
    sock.write('\r\n')
    sock.write(json_body)


def start_server():
    server = ThreadingUnixStreamServer(unix_socket_path,
                                       RequestHandler)
    server.serve_forever()


def cleanup():
    """Used for forced cleanup"""
    if os.path.exists(unix_socket_path):
        os.remove(unix_socket_path)
