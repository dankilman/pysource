import socket

from pysource.env import unix_socket_path

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.connect(unix_socket_path)
try:
    sock.sendall('one two three')
    response = sock.recv(1024)
    print "Received: {}".format(response)
finally:
    sock.close()
