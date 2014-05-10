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
from SocketServer import (ThreadingUnixStreamServer,
                          StreamRequestHandler)

from pysource import env
from pysource import protocol
from pysource import request_context
from pysource import registry


def _handle_source_register(payload):
    source_content = payload['source_content']
    exec(source_content, globals())
    names = [reg.name for reg in request_context.registered]
    return {'names': names}


def _handle_list_registered(_):
    names = [reg.name for reg in registry.get_registered()]
    return {'names': names}


def _handle_run_function(payload):
    function_name = payload['name']
    args = payload['args']
    result = registry.run_function(function_name, args)
    return {'result': result}


def _handle(req_type, payload):
    handler = lambda _: 'none'
    if req_type == protocol.SOURCE_REGISTER_REQUEST:
        handler = _handle_source_register
    elif req_type == protocol.RUN_FUNCTION_REQUEST:
        handler = _handle_run_function
    elif req_type == protocol.LIST_REGISTERED:
        handler = _handle_list_registered
    return handler(payload)


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
            res_status = protocol.RESPONSE_STATUS_OK
        except Exception, e:
            res_status = protocol.RESPONSE_STATUS_ERROR
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


def run():
    server = ThreadingUnixStreamServer(env.unix_socket_path,
                                       RequestHandler)
    server.serve_forever()
