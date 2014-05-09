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


from pysource import function


@function
def fun1(name, name2, name3):
    return 'name: {0}, name2: {1}, name3: {2}'.format(name, name2, name3)


@function
def fun2(name):
    return 'name: {0}'.format(name)


@function
def fun3(name):
    return 'fun3: {0}'.format(name)
