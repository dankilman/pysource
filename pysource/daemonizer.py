import os
import sys
import errno

import daemon
import lockfile

pidfile_dir = os.path.expanduser('~/.pysource')
pidfile_path = os.path.join(pidfile_dir, 'pidfile')
pidfile = lockfile.FileLock(pidfile_path)

context = daemon.DaemonContext(
    pidfile=pidfile,
    stdout=sys.stdout,
    stderr=sys.stderr
)

def start():
    make_pysource_dir()
    try:
        pidfile.acquire(timeout=-1)
        pidfile.release()
    except lockfile.AlreadyLocked:
        print 'daemon already started'
        return
    with context:
        from time import sleep
        sleep(1)

def make_pysource_dir():
    try:
        os.mkdir(pidfile_dir)
    except OSError, e:
        if e.errno != errno.EEXIST:
            raise
