import os
import sys
import errno
import signal

import daemon
import lockfile

_pidfile_dir = os.path.expanduser('~/.pysource')
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
        _write_pid()
        from time import sleep
        sleep(100)


def stop():
    if not _pidfile.is_locked():
        print 'daemon not running'
        return
    os.kill(_read_pid(), signal.SIGTERM)


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
