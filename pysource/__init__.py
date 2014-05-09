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


import functools
import threading
import uuid
import argh

from pysource import registry


class RequestContext(threading.local):

    def __init__(self):
        super(RequestContext, self).__init__(self)
        self.uuid = uuid.uuid4()
        self.registered = []

    def add_registered(self, function_holder):
        self.registered.append(function_holder)
request_context = RequestContext()


def function(func, *args, **kwargs):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    registry.register(func, wrapper, request_context)
    return wrapper


class ExecutionError(argh.CommandError):
    pass