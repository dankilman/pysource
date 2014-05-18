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


from base import WithDaemonTestCase
from pysource.tests import command


class SourceRegisteredTest(WithDaemonTestCase):

    def test_source_registered(self):
        self.run_pysource_script([
            command.source(self.valid_source_path),
        ])
        output = self.run_pysource_script([
            command.source_registered(),
            command.list_registered()
        ]).split('\n')
        self.assertIn('function1', output)
        self.assertIn('function2', output)
        self.assertIn('function3 (piped)', output)
        self.assertEqual('function1', self.run_pysource_script([
            command.source_registered(),
            command.run('function1')
        ]))
        self.assertEqual('function2', self.run_pysource_script([
            command.source_registered(),
            command.run('function2')
        ]))

    def test_source_registered_verbose(self):
        self.run_pysource_script([
            command.source(self.valid_source_path),
        ])
        output = self.run_pysource_script([
            command.source_registered(verbose=True),
            command.list_registered()
        ]).split('\n')
        self.assertIn('function1 function sourced.', output)
        self.assertIn('function2 function sourced.', output)
        self.assertIn('function3 function sourced.', output)
