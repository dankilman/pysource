import os
import sys
import errno
import signal
import time

import daemon
import lockfile

from pysource import env, server

_pidfile_dir = env.pysource_dir
_pidfile_path = os.path.join(_pidfile_dir, 'pidfile')
_pidfile = lockfile.FileLock(_pidfile_path)

_context = daemon.DaemonContext(
    pidfile=_pidfile,
    stdout=sys.stdout,
    stderr=sys.stderr
)


def start():
    _make_pysource_dir()
    if _pidfile.is_locked():
        print 'daemon already started'
        return
    with _context:
        print 'daemon started'
        _write_pid()
        server.run()


def stop():
    if not _pidfile.is_locked():
        print 'daemon not running'
        return
    os.kill(_read_pid(), signal.SIGTERM)
    os.remove(env.unix_socket_path)


def restart():
    stop()
    time.sleep(1)
    start()


def _write_pid():
    with open(_pidfile.lock_file, 'w') as f:
        f.write(str(os.getpid()))


def _read_pid():
    with open(_pidfile.lock_file, 'r') as f:
        return int(f.read())


def _make_pysource_dir():
    try:
        os.mkdir(_pidfile_dir)
    except OSError, e:
        if e.errno != errno.EEXIST:
            raise
