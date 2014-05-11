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


import argh

from pysource import daemonizer
from pysource import client


def daemon(action):
    if action == 'start':
        started = daemonizer.start()
        if not started:
            return 'Daemon already started'
    elif action == 'stop':
        stopped = daemonizer.stop()
        if stopped:
            return 'Daemon stopped'
        else:
            return 'Daemon not running'
    elif action == 'restart':
        daemonizer.restart()
    elif action == 'status':
        status, pid = daemonizer.status()
        if status == daemonizer.STATUS_STOPPED:
            return 'Daemon is (probably) stopped'
        elif status == daemonizer.STATUS_CORRUPTED:
            return 'Daemon pidfile exists but process does not seem ' \
                   'to be running (pid: {0}). You should probably clean ' \
                   'the files in ~/.pysource and manually check if there is' \
                   ' a daemon running somewhere'.format(pid)
        else:
            return 'Daemon is (probably) running (pid: {0})'.format(pid)
    else:
        raise argh.CommandError('unrecognized action: {0} '
                                '[valid: start, stop, restart, status]'
                                .format(action))


def list_registered():
    names = client.list_registered()
    yield 'Registered functions:'
    for name in names:
        yield name


def source_registered(verbose=False):
    return client.source_registered(verbose=verbose)


def source_named(function_name, verbose=False):
    return client.source_named(function_name,
                               verbose=verbose)


def source(source_path, verbose=False):
    return client.source_register(source_path,
                                  verbose=verbose)


def run(function_name, *args):
    return client.run_function(function_name, args)


def main():
    argh.dispatch_commands([
        daemon,
        source,
        run,
        list_registered,
        source_registered,
        source_named
    ], completion=False)


if __name__ == '__main__':
    main()
