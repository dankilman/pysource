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

from pysource import shell
from pysource import ExecutionError
from pysource import handlers


def source_register(source_path, verbose=False):
    if not os.path.exists(source_path):
        raise ExecutionError('{0} does not exist'.format(source_path))
    with open(source_path, 'r') as f:
        source_content = f.read()
    result = handlers.source_register.remote(source_content=source_content)
    return shell.create_shell_functions(result['descriptors'],
                                        verbose=verbose)


def run_function(function_name, args):
    result = handlers.run_function.remote(name=function_name, args=args)
    return result['result']


def run_piped_function(function_name, args):
    handlers.run_piped_function.remote(name=function_name, args=args)


def list_registered():
    result = handlers.list_registered.remote()
    return result['descriptors']


def source_registered(verbose=False):
    return shell.create_shell_functions(list_registered(),
                                        verbose=verbose)


def source_named(function_name, piped=False, verbose=False):
    descriptor = {'name': function_name, 'piped': piped}
    return shell.create_shell_functions([descriptor],
                                        verbose=verbose)
