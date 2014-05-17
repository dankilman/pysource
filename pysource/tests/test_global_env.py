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


class GlobalEnvTest(WithDaemonTestCase):

    def test_global_env_emtpy(self):
        output = self.run_pysource_script([
            command.source_def('''function1():
    return ",".join(globals().keys())'''),
            command.run('function1')
        ]).split(',')
        self.assertEqual(len(output), 8)
        self.assertIn('function1', output)
        self.assertIn('pysource', output)
        self.assertIn('__pysource_evaluate__', output)
        self.assertIn('__builtins__', output)
        self.assertIn('__file__', output)
        self.assertIn('__package__', output)
        self.assertIn('__name__', output)
        self.assertIn('__doc__', output)
