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


class UpdateEnvTest(WithDaemonTestCase):

    def test_update_env(self):
        output = self.run_pysource_script([
            command.source_inline('from pysource import env as e'),
            command.source_def('function1(): return e.NEW_ENV'),
            command.run('function1')])
        self.assertEqual(output, str(None))
        new_env_value = 'NEW_ENV_VALUE'
        output = self.run_pysource_script([
            command.update_env(NEW_ENV=new_env_value),
            command.source_named('function1'),
            command.run('function1')])
        self.assertEqual(output, new_env_value)

    def test_update_env_verbose(self):
        output = self.run_pysource_script([
            command.update_env(verbose=True)])
        self.assertEqual(output, 'Environment updated')

    def test_update_env_no_daemon(self):
        self.daemon_stop(wait_for_stopped=True)
        self.assertRaises(sh.ErrorReturnCode,
                          self.run_pysource_script,
                          [command.update_env()])
