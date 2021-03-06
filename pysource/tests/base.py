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


import tempfile
from unittest import TestCase
from os import path
import sys
import shutil
import time
import os

import sh
sh.ErrorReturnCode.truncate_cap = 2 ** 32

from pysource import config
from pysource import daemonizer
from pysource.config import PYSOURCE_HOME_ENV

from pysource.tests import command


def bake(sh_command):
    return sh_command.bake(_out=lambda line: sys.stdout.write(line),
                           _err=lambda line: sys.stderr.write(line))
bash = bake(sh.bash)
pkill = bake(sh.pkill)


class BaseTestCase(TestCase):

    def setUp(self):
        workdir = tempfile.mkdtemp(suffix='', prefix='pysource-test-')
        self.workdir = path.abspath(workdir)
        config.pysource_dir = self.workdir
        self.addCleanup(self.cleanup)
        self.valid_source_path = self.resource_path('functions.py')
        self.error_source_path = self.resource_path('with_error.py')
        self.pipes_source_path = self.resource_path('pipes.py')

    def tearDown(self):
        pass

    def kill_daemon(self):
        pkill('-9', 'pysource.main', f=True, _ok_code=[0, 1]).wait()

    def cleanup(self):
        self.kill_daemon()
        shutil.rmtree(self.workdir)

    def run_pysource_script(
            self,
            commands=(),
            bg=False,
            env=None,
            strip=True,
            _in=None,
            _out=None):
        commands = list(commands)
        script_path = self._create_script(commands)
        if env is None:
            env = os.environ.copy()
        env[PYSOURCE_HOME_ENV] = self.workdir
        conf = {'_env': env}
        if _in is not None:
            conf['_in'] = _in
            conf['_in_bufsize'] = 0
        if _out is not None:
            conf['_out'] = _out
            conf['_out_bufsize'] = 0
        if bg:
            conf['_bg'] = True
            bash(script_path, **conf)
        else:
            output = sh.bash(script_path, **conf).wait()
            if strip:
                output = output.strip()
            return output

    def _create_script(self, commands):
        script_path = tempfile.mktemp(prefix='pysource-', dir=self.workdir)
        with open(script_path, 'w') as f:
            set_e_command = 'set -e'
            source_command = 'source $(which pysource.sh)'
            commands = [set_e_command, source_command] + commands
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

    def daemon_start(self, wait_for_started=False):
        self.run_pysource_script([
            command.daemon('start')
        ], bg=True)
        if wait_for_started:
            self.wait_for_status(daemonizer.STATUS_RUNNING)

    def daemon_stop(self, wait_for_stopped=False):
        self.run_pysource_script([
            command.daemon('stop')
        ], bg=True)
        if wait_for_stopped:
            self.wait_for_status(daemonizer.STATUS_STOPPED)

    def daemon_restart(self, wait_for_started=False):
        self.run_pysource_script([
            command.daemon('restart')
        ], bg=True)
        if wait_for_started:
            self.wait_for_status(daemonizer.STATUS_RUNNING)

    def daemon_status(self):
        return self.run_pysource_script([
            command.daemon('status')
        ], bg=False)

    def resource_path(self, resource_name):
        return path.abspath(path.join(path.dirname(__file__),
                                      'resources',
                                      resource_name))


class WithDaemonTestCase(BaseTestCase):

    def setUp(self):
        super(WithDaemonTestCase, self).setUp()
        self.daemon_start(wait_for_started=True)
