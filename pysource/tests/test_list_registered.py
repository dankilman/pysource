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


class ListRegisteredTest(WithDaemonTestCase):

    def test_list_empty(self):
        self.assertEqual(self.list_registered(),
                         'No functions registered')

    def test_list_full(self):
        self.source_def('function1(): pass')
        self.source_def('function2(): pass', piped=True)
        output = self.list_registered().split('\n')
        self.assertIn('function1', output)
        self.assertIn('function2 (piped)', output)
