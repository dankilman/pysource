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

import os
from unittest import TestCase

from pysource import env


class SugaredEnvTest(TestCase):

    def test_existing(self):
        env_home = os.environ.get('HOME')
        self.assertIsNotNone(env_home)
        self.assertEqual(env.HOME, env_home)

    def test_non_existing(self):
        env_non_existing = os.environ.get('I_DO_NOT_EXIST')
        self.assertIsNone(env_non_existing)
        self.assertEqual(env.I_DO_NOT_EXIST, env_non_existing)
