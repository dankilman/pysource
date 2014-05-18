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


class SourceDefTest(WithDaemonTestCase):

    def test_source_def_explicit(self):
        output = self.run_pysource_script([
            command.source_def_explicit('function1(): return 1'),
            command.run('function1')
        ])
        self.assertEqual(output, '1')

    def test_source_def(self):
        output = self.run_pysource_script([
            command.source_def('function1(): return 1'),
            command.run('function1')
        ])
        self.assertEqual(output, '1')

    def test_source_multi_line(self):
        output = self.run_pysource_script([
            command.source_def('''function1():
    a = 3
    b = 2
    return a + b
'''),
            command.run('function1')
        ])
        self.assertEqual(output, '5')

    def test_source_def_piped(self):
        output = self.run_pysource_script([
            command.source_def('function1(): return 1', piped=True),
            command.list_registered()
        ]).split('\n')
        self.assertIn('function1 (piped)', output)

    def test_source_def_verbose(self):
        output = self.run_pysource_script([
            command.source_def('function1(): return 1', verbose=True),
        ]).split('\n')
        self.assertIn('function1 function sourced.', output)

    def test_source_def_verbose_and_piped(self):
        output = self.run_pysource_script([
            command.source_def('function1(): return 1',
                               verbose=True,
                               piped=True),
        ])
        self.assertIn('run-piped function1', output)
