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


import copy

from pysource import arguments


class FunctionHolder(object):

    def __init__(self, function, wrapper, piped):
        self.function = function
        self.wrapper = wrapper
        self.type_spec = arguments.ArgTypeSpec(function, piped)
        self.name = function.__name__
        self.piped = piped

    def run(self, args):
        parsed_args = self.type_spec.parse(args)
        return self.wrapper(*parsed_args)


registered = {}


def register(function, wrapper, request_context, piped):
    holder = FunctionHolder(function, wrapper, piped)
    registered[holder.name] = holder
    request_context.add_registered(holder)


def run_function(function_name, args):
    if function_name not in registered:
        raise RuntimeError('{0} not registered'.format(function_name))
    return registered[function_name].run(args)


def get_registered():
    return copy.copy(registered.values())
