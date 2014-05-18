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


class RunTest(WithDaemonTestCase):

    def setUp(self):
        super(RunTest, self).setUp()
        self.piped = False

    def test_run_explicit(self):
        self._test_run_explicit(self._run_explicit_command(self.piped))

    def test_run_no_args(self):
        output = self.run_pysource_script([
            command.source_def('function1(): return 1',
                               piped=self.piped),
            command.run('function1')
        ])
        self.assertEqual(output, '1')

    def test_run_with_args(self):
        name = 'john'
        output = self.run_pysource_script([
            command.source_def('function1(name): return name*2',
                               piped=self.piped),
            command.run('function1', name)
        ])
        self.assertEqual(output, name*2)

    def test_run_with_typed_args(self):
        number = 3
        output = self.run_pysource_script([
            command.source_def('function1(number=int): return number**3',
                               piped=self.piped),
            command.run('function1', number)
        ])
        self.assertEqual(output, str(number**3))

    def test_run_with_varargs(self):
        names = ['john', 'doe']
        output = self.run_pysource_script([
            command.source_def('function1(*names): return list(names+names)',
                               piped=self.piped),
            command.run('function1', *names)
        ])
        self.assertEqual(output, str(names+names))

    def test_run_with_kwargs(self):
        output = self.run_pysource_script([
            command.source_def('function1(**kwargs): return 1',
                               piped=self.piped),
            command.run('function1')
        ])
        self.assertEqual(output, '1')

    def test_run_with_args_and_varargs(self):
        name = 'jane'
        names = ['john', 'doe']
        args = [name] + names
        output = self.run_pysource_script([
            command.source_def('''function1(name, *names):
    return [name]+list(names)''', piped=self.piped),
            command.run('function1', *args)
        ])
        self.assertEqual(output, str(args))

    def test_run_too_many_args_no_varargs(self):
        self.assertRaises(sh.ErrorReturnCode,
                          self.run_pysource_script,
                          [
                              command.source_def('function1(): pass',
                                                 piped=self.piped),
                              command.run('function1', 'arg')
                          ])

    def test_run_too_few_args_no_varargs(self):
        self.assertRaises(sh.ErrorReturnCode,
                          self.run_pysource_script,
                          [
                              command.source_def('function1(arg): pass',
                                                 piped=self.piped),
                              command.run('function1')
                          ])

    def test_run_too_few_args_with_varargs(self):
        self.assertRaises(sh.ErrorReturnCode,
                          self.run_pysource_script,
                          [
                              command.source_def('function1(ar, *args): pass',
                                                 piped=self.piped),
                              command.run('function1')
                          ])

    def test_run_no_function(self):
        self.assertRaises(sh.ErrorReturnCode,
                          self.run_pysource_script,
                          [command.source_named('function1',
                                                piped=self.piped),
                           command.run('function1')])

    def test_run_with_run_piped_mode(self):
        self.assertRaises(sh.ErrorReturnCode,
                          self._test_run_explicit,
                          self._run_explicit_command(not self.piped))

    def _test_run_explicit(self, run_explicit_command):
        output = self.run_pysource_script([
            command.source_def('function1(): return 1',
                               piped=self.piped),
            run_explicit_command('function1')
        ])
        self.assertEqual(output, '1')

    def _run_explicit_command(self, piped):
        if piped:
            return command.run_piped_explicit
        else:
            return command.run_explicit
