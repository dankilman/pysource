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


from base import BaseTestCase


class BashCompletionTest(BaseTestCase):

    def completion(self, *args):
        cmd = ['pysource'] + list(args)
        partial_word = cmd[-1]
        cmdline = ' '.join(cmd)
        reg_exp = r"s/.*-F \\([^ ]*\\) .*/\\1/"
        return self.run_pysource_script([
            'export COMP_LINE={}'.format(cmdline),
            'export COMP_WORDS=({})'.format(cmdline),
            'export COMP_CWORD={}'.format(cmd.index(partial_word)),
            'export COMP_POINT={}'.format(len(cmdline)),
            '$(complete -p {} | sed "{}") && echo ${{COMPREPLY[*]}}'
            .format(cmd[0], reg_exp),
        ]).split(' ')

    def test_pysource_completion(self):
        completion = self.completion('')
        self.assertIn('daemon', completion)
        self.assertIn('list-registered', completion)
        self.assertIn('update-env', completion)
        self.assertIn('source-registered', completion)
        self.assertIn('source-named', completion)
        self.assertIn('source-def', completion)
        self.assertIn('source-inline', completion)
        self.assertIn('source', completion)
        self.assertIn('run', completion)
        self.assertIn('run-piped', completion)

    def test_pysource_daemon_completion(self):
        completion = self.completion('daemon', '')
        self.assertIn('start', completion)
        self.assertIn('stop', completion)
        self.assertIn('restart', completion)
        self.assertIn('status', completion)
