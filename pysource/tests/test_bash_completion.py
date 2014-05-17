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

    def assert_completion(self, expected, args=None):
        args = args or []
        args += ['']
        cmd = ['pysource'] + list(args)
        partial_word = cmd[-1]
        cmdline = ' '.join(cmd)
        reg_exp = r"s/.*-F \\([^ ]*\\) .*/\\1/"
        completions = self.run_pysource_script([
            'export COMP_LINE={}'.format(cmdline),
            'export COMP_WORDS=({})'.format(cmdline),
            'export COMP_CWORD={}'.format(cmd.index(partial_word)),
            'export COMP_POINT={}'.format(len(cmdline)),
            '$(complete -p {} | sed "{}") && echo ${{COMPREPLY[*]}}'
            .format(cmd[0], reg_exp),
        ]).split(' ')
        self.assertEqual(len(expected), len(completions))
        for expected_completion in expected:
            self.assertIn(expected_completion, completions)

    def test_pysource_completion(self):
        self.assert_completion(
            expected=[
                'daemon',
                'list-registered',
                'update-env',
                'source-registered',
                'source-named',
                'source-def',
                'source-inline',
                'source',
                'run',
                'run-piped'
            ])

    def test_pysource_daemon_completion(self):
        self.assert_completion(
            args=['daemon'],
            expected=[
                'start',
                'stop',
                'restart',
                'status'
            ])
