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

import time
import tempfile
import shutil
from unittest import TestCase
from os import path
import sys

import sh


from pysource import config
from pysource import daemonizer


def bake(command):
    return command.bake(_out=lambda line: sys.stdout.write(line),
                        _err=lambda line: sys.stderr.write(line))
bash = bake(sh.bash)
pkill = bake(sh.pkill)


class DaemonTest(TestCase):

    def setUp(self):
        workdir = tempfile.mkdtemp(suffix='', prefix='pysource-test-')
        self.workdir = path.abspath(workdir)
        config.pysource_dir = self.workdir
        self.addCleanup(self.cleanup)

    def tearDown(self):
        pass

    def _kill_daemon(self):
        pkill('-9', 'pysource.main', f=True, _ok_code=[0, 1]).wait()

    def cleanup(self):
        self._kill_daemon()
        shutil.rmtree(self.workdir)

    def _run(self, commands, bg=False):
        commands = list(commands)
        script_path = self._create_script(commands)
        if bg:
            bash(script_path, _bg=bg)
        else:
            return sh.bash(script_path)

    def _create_script(self, commands):
        script_path = tempfile.mktemp(dir=self.workdir)
        with open(script_path, 'w') as f:
            export_command = 'export PYSOURCE_HOME={}'.format(self.workdir)
            source_command = 'source $(which pysource.sh)'
            commands = [export_command, source_command] + commands
            script_content = '\n'.join(commands)
            f.write(script_content)
        return script_path

    def _repetitive(self, func, timeout=5, interval=0.1):
        end = time.time() + timeout
        while True:
            try:
                return func()
            except AssertionError:
                if time.time() < end:
                    time.sleep(interval)
                else:
                    raise

    def wait_for_status(self, expected_status):
        def run():
            status, pid = daemonizer.status()
            self.assertEqual(status, expected_status)
        self._repetitive(run)

    def _start_daemon(self):
        self._run([
            'pysource daemon start'
        ], bg=True)

    def _stop_daemon(self):
        self._run([
            'pysource daemon stop'
        ], bg=True)

    def _restart_daemon(self):
        self._run([
            'pysource daemon restart'
        ], bg=True)

    def _status_daemon(self):
        return self._run([
            'pysource daemon status'
        ], bg=False)

    def test_start_not_running(self):
        self._start_daemon()
        self.wait_for_status(daemonizer.STATUS_RUNNING)

    def test_start_already_running(self):
        self.test_start_not_running()
        # this time daemon is actually already running
        self.test_start_not_running()

    def test_start_corrupted(self):
        self.test_start_not_running()
        # kill -9 puts daemon in corrupted state
        self._kill_daemon()
        self.test_start_not_running()

    def test_stop_running(self):
        self.test_start_not_running()
        self._stop_daemon()
        self.wait_for_status(daemonizer.STATUS_STOPPED)

    def test_stop_not_running(self):
        self._stop_daemon()
        self.wait_for_status(daemonizer.STATUS_STOPPED)

    def test_stop_corrupted(self):
        self.test_start_not_running()
        # kill -9 puts daemon in corrupted state
        self._kill_daemon()
        self.wait_for_status(daemonizer.STATUS_CORRUPTED)

    def test_restart_not_running(self):
        self._restart_daemon()
        self.wait_for_status(daemonizer.STATUS_RUNNING)

    def test_restart_running(self):
        self.test_start_not_running()
        # it is now running
        self.test_restart_not_running()

    def test_restart_corrupted(self):
        self.test_start_not_running()
        self._kill_daemon()
        self.test_restart_not_running()

    def test_status_running(self):
        self.test_start_not_running()
        self.assertTrue('Daemon is (probably) running'
                        in self._status_daemon())

    def test_status_not_running(self):
        self.assertEqual('Daemon is (probably) stopped',
                         self._status_daemon().strip())

    def test_status_corrupted(self):
        self.test_start_not_running()
        self._kill_daemon()
        self.assertTrue('Daemon pidfile exists but'
                        in self._status_daemon())

    def test_unknown_action(self):
        self.assertRaises(sh.ErrorReturnCode, self._run,
                          ['pysource daemon idonotexist'])
