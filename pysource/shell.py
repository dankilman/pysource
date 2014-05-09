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


def create_shell_functions(function_names):
    return ''.join([_create_shell_function(name)
                   for name in function_names])


def _create_shell_function(function_name):
    return '''%(function_name)s()
{
    __pysource_run %(function_name)s "$@"
}

''' % dict(function_name=function_name)
