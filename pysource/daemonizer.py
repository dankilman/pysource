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
import sys
import errno
import signal
import time

import daemon
import lockfile

from pysource import env, transport

_pidfile_dir = env.pysource_dir
_pidfile_path = os.path.join(_pidfile_dir, 'pidfile')
_pidfile = lockfile.FileLock(_pidfile_path)

_context = daemon.DaemonContext(
    pidfile=_pidfile,
    stdout=sys.stdout,
    stderr=sys.stderr
)


def start(force):
    _make_pysource_dir()
    if force:
        _pidfile.break_lock()
        if os.path.exists(env.unix_socket_path):
            os.remove(env.unix_socket_path)
    elif _pidfile.is_locked():
        return False
    with _context:
        _write_pid()
        transport.start_server()


def stop():
    if not _pidfile.is_locked():
        return False
    os.kill(_read_pid(), signal.SIGTERM)
    os.remove(env.unix_socket_path)
    return True


def restart(force):
    if _pidfile.is_locked() and not force:
        stop()
        time.sleep(1)
    start(force)


def status():
    stat = 'stopped'
    pid = None
    if _pidfile.is_locked():
        pid = _read_pid()
        stat = 'running' if _process_is_running(pid) else 'corrupted'
    return stat, pid


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


def _process_is_running(pid):
    try:
        os.kill(pid, signal.SIG_DFL)
    except OSError, e:
        return e.errno != errno.ESRCH
    else:
        return True
