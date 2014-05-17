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
import socket

from base import BaseTestCase


class DaemonFilesTest(BaseTestCase):

    def assert_valid_state(self, running, expected_extra):
        # 3 daemon files + the extra are test script file
        files = os.listdir(self.workdir)
        if running:
            self.assertEqual(3 + expected_extra, len(files))
            self.assertIn('pidfile.lock', files)
            self.assertIn('socket', files)
            for file_name in files:
                if file_name.startswith('{}-'.format(socket.gethostname())):
                    break
            else:
                self.fail('Failed finding daemon specific lock file')
        extra_count = len([f for f in files if f.startswith('pysource-')])
        self.assertEqual(expected_extra, extra_count)

    def test_daemon_running(self):
        self.daemon_start(wait_for_started=True)
        self.assert_valid_state(running=True,
                                expected_extra=1)

    def test_daemon_stopped(self):
        self.test_daemon_running()
        self.daemon_stop(wait_for_stopped=True)
        self.assert_valid_state(running=False,
                                expected_extra=2)

    def test_daemon_restarted(self):
        self.test_daemon_running()
        self.daemon_restart(wait_for_started=True)
        self.assert_valid_state(running=True,
                                expected_extra=2)
