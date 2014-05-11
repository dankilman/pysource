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


from pysource import request_context
from pysource import registry
from pysource import remote_call


@remote_call
def source_register(source_content):
    exec(source_content, globals())
    names = [reg.name for reg in request_context.registered]
    return {'names': names}


@remote_call
def list_registered():
    names = [reg.name for reg in registry.get_registered()]
    return {'names': names}


@remote_call
def run_function(name, args):
    result = registry.run_function(name, args)
    return {'result': result}
