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


class SourceInlineTest(WithDaemonTestCase):

    def test_source_inline(self):
        output = self.run_pysource_script([
            command.source_inline('name=3'),
            command.source_def('function1(): return name'),
            command.run('function1')
        ])
        self.assertEqual(output, '3')

    def test_source_inline_multi_line(self):
        output = self.run_pysource_script([
            command.source_inline('''name="John Doe"
age=13
'''),
            command.source_def('function1(): return name,age'),
            command.run('function1')
        ])
        self.assertEqual(output, str([u"John Doe", 13]))
