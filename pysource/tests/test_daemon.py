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


import sh

from pysource import daemonizer

from base import BaseTestClass


class DaemonTest(BaseTestClass):

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
