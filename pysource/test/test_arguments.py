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


from unittest import TestCase

from pysource.arguments import ArgTypeSpec


class ArgumentsTest(TestCase):

    def _assert_valid_parsing(self, fun, args, expected_parsed_args):
        self.assertEqual(ArgTypeSpec(fun).parse(args),
                         expected_parsed_args)

    def test_plain_args(self):
        def fun(arg1):
            pass
        self._assert_valid_parsing(fun, ['1'], ['1'])

    def test_typed_args(self):
        def fun(arg1=int, arg2=float, arg3=str):
            pass
        self._assert_valid_parsing(fun, ['1', '2.2', '3'], [1, 2.2, '3'])

    def test_mixed_args(self):
        def fun(arg1, arg2=int):
            pass
        self._assert_valid_parsing(fun, ['1', '2'], ['1', 2])
