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


from base import BaseTestCase
from pysource.tests import command


class NoDaemonTest(BaseTestCase):

    def assert_error(self, *commands):
        self.assertRaises(sh.ErrorReturnCode,
                          self.run_pysource_script,
                          commands)

    def test_list_registered_no_daemon(self):
        self.assert_error(command.list_registered())

    def test_run_no_daemon(self):
        self.assert_error(command.source_named('function1'),
                          command.run('function1'))

    def test_source_no_daemon(self):
        self.assert_error(command.source(self.valid_source_path))

    def test_source_def_no_daemon(self):
        self.assert_error(command.source_def('function1(): pass'))

    def test_source_inline_no_daemon(self):
        self.assert_error(command.source_inline('1'))

    def test_source_registered_no_daemon(self):
        self.assert_error(command.source_registered())

    def test_update_env_no_daemon(self):
        self.assert_error(command.update_env())

    def test_source_named_no_daemon(self):
        output = self.run_pysource_script([
            command.source_named('function1', verbose=True),
        ])
        self.assertIn('run function1', output)
        output = output.split('\n')
        self.assertIn('function1 function sourced.', output)