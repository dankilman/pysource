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


import socket
import json
import os

from pysource.env import unix_socket_path
from pysource import protocol
from pysource import shell
from pysource import ExecutionError


def source_register(source_path, verbose=False):
    if not os.path.exists(source_path):
        raise ExecutionError('{0} does not exist'.format(source_path))
    with open(source_path, 'r') as f:
        source_content = f.read()
    result = do_request(
        protocol.SOURCE_REGISTER_REQUEST, {
            'source_content': source_content
        })
    return shell.create_shell_functions(result['names'],
                                        verbose=verbose)


def run_function(function_name, args):
    result = do_request(
        protocol.RUN_FUNCTION_REQUEST, {
            'name': function_name,
            'args': args
        })
    return result['result']


def list_registered():
    result = do_request(protocol.LIST_REGISTERED, {})
    return result['names']


def source_registered(verbose=False):
    return shell.create_shell_functions(list_registered(),
                                        verbose=verbose)


def source_named(function_name, verbose=False):
    return shell.create_shell_functions([function_name],
                                        verbose=verbose)


def do_request(req_type, payload):
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(unix_socket_path)
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
        if res_body['status'] == protocol.RESPONSE_STATUS_ERROR:
            error = res_body_payload['error']
            raise ExecutionError('execution failed: {0}'.format(error))
        return res_body_payload
    finally:
        req.close()
        res.close()
        sock.close()
