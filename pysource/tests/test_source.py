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

from base import WithDaemonTestCase
from pysource.tests import command


class SourceTest(WithDaemonTestCase):

    def test_source_explicit(self):
        output = self.run_pysource_script([
            command.source_explicit(self.valid_source_path),
            command.list_registered()
        ]).split('\n')
        self.assertIn('function1', output)
        self.assertIn('function2', output)
        self.assertIn('function3 (piped)', output)
        self.assertEqual('function1', self.run_pysource_script([
            command.source_named('function1'),
            command.run('function1')
        ]))
        self.assertEqual('function2', self.run_pysource_script([
            command.source_named('function2'),
            command.run('function2')
        ]))

    def test_source(self):
        output = self.run_pysource_script([
            command.source(self.valid_source_path),
            command.list_registered()
        ]).split('\n')
        self.assertIn('function1', output)
        self.assertIn('function2', output)
        self.assertIn('function3 (piped)', output)

    def test_source_verbose(self):
        output = self.run_pysource_script([
            command.source(self.valid_source_path, verbose=True)
        ])

        self.assertIn('run function1', output)
        self.assertIn('run function2', output)
        self.assertIn('run-piped function3', output)

        output = output.split('\n')
        self.assertIn('function1 function sourced.', output)
        self.assertIn('function2 function sourced.', output)
        self.assertIn('function3 function sourced.', output)

    def test_source_with_errors(self):
        self.assertRaises(sh.ErrorReturnCode,
                          self.run_pysource_script,
                          [command.source(self.error_source_path)])

    def test_source_doesnt_exist(self):
        self.assertRaises(sh.ErrorReturnCode,
                          self.run_pysource_script,
                          [command.source(self.valid_source_path + '_')])
