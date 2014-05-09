import socket

from pysource.env import unix_socket_path
from pysource import protocol


def source_register(source_path):
    with open(source_path, 'r') as f:
        source_content = f.read()
    def handler(req, res):
        req.write(protocol.CLIENT_SOURCE_REGISTER_REQUEST)
        req.write('\r\n')
        req.write(len(source_content))
        req.write('\r\n')
        req.write(source_content)
        res_type = res.read(1)
        print res.read()
    _do_request(handler)


def _do_request(handler):
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(unix_socket_path)
    req = sock.makefile('wb', 0)
    res = sock.makefile('rb', -1)
    try:
        handler(req, res)
    finally:
        req.close()
        res.close()
        sock.close()
