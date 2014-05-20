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


from sys import stdout


from base import WithDaemonTestCase
from pysource.tests import command


class PipingTest(WithDaemonTestCase):

    def setUp(self):
        super(PipingTest, self).setUp()
        self.run_pysource_script([command.source(self.pipes_source_path)])

    def piped(self, commands, _in=None, _out=None):
        pipe = ' | '.join(commands)
        commands = [command.source_registered(), pipe]
        return self.run_pysource_script(commands,
                                        strip=False,
                                        _in=_in,
                                        _out=_out)

    def _test(self):
        import time

        def _in():
            for i in range(1, 10):
                yield str(i)
                time.sleep(1)

        global timestamp
        timestamp = time.time()

        def _out(b):
            global timestamp
            prev = timestamp
            timestamp = time.time()
            stdout.write('{}: {}\n'.format(b, timestamp-prev))

        print self.piped([command.run('py_echo')],
                         _in=_in(), _out=_out)
