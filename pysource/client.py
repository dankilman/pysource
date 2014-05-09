import socket
import json

from pysource.env import unix_socket_path
from pysource import protocol


def source_register(source_path):
    with open(source_path, 'r') as f:
        source_content = f.read()
    result = do_request(
        protocol.SOURCE_REGISTER_REQUEST, {
            'source_content': source_content
        })
    return result


def run_function(function_name, args):
    result = do_request(
        protocol.RUN_FUNCTION_REQUEST, {
            'name': function_name,
            'args': args
        })
    return result


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
        return json.loads(res.read(res_body_len))['payload']
    finally:
        req.close()
        res.close()
        sock.close()
