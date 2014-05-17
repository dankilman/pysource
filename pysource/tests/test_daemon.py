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

from unittest import TestCase


class DaemonTest(TestCase):

    def test_start_not_running(self):
        self.fail()

    def test_start_already_running(self):
        self.fail()

    def test_start_corrupted(self):
        self.fail()

    def test_stop_running(self):
        self.fail()

    def test_stop_not_running(self):
        self.fail()

    def test_stop_corrupted(self):
        self.fail()

    def test_restart_not_running(self):
        self.fail()

    def test_restart_running(self):
        self.fail()

    def test_restart_corrupted(self):
        self.fail()

    def test_status_running(self):
        self.fail()

    def test_status_not_running(self):
        self.fail()

    def test_status_corrupted(self):
        self.fail()

    def test_unknown_action(self):
        self.fail()
