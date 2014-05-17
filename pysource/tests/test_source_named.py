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


class SourceNamedTest(WithDaemonTestCase):

    def test_source_named(self):
        self.run_pysource_script([
            command.source_def('function1(): return 1'),
        ])
        output = self.run_pysource_script([
            command.source_named('function1'),
            command.run('function1')
        ])
        self.assertEqual(output, '1')

    def test_source_named_piped(self):
        self.run_pysource_script([
            command.source_def('function1(): return 1', piped=True),
        ])
        output = self.run_pysource_script([
            command.source_named('function1', piped=True),
            command.run('function1')
        ])
        self.assertEqual(output, '1')

    def test_source_named_verbose(self):
        output = self.run_pysource_script([
            command.source_named('function1', verbose=True),
        ])
        self.assertIn('run function1', output)
        output = output.split('\n')
        self.assertIn('function1 function sourced.', output)

    def test_source_named_verbose_and_piped(self):
        output = self.run_pysource_script([
            command.source_named('function1',
                                 verbose=True,
                                 piped=True),
            ])
        self.assertIn('run-piped function1', output)

    def test_source_def_no_daemon(self):
        self.daemon_stop(wait_for_stopped=True)
        self.test_source_named_verbose()
