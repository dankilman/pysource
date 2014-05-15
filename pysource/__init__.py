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

import sys
import functools
import threading
import argh

remote_call_handlers = {}


def remote_call(func):
    request_type = func.__name__

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    remote_call_handlers[request_type] = wrapper

    def remote(**kwargs):
        # import here to avoid cyclic dependencies
        from pysource.transport import do_regular_client_request
        return do_regular_client_request(request_type, kwargs)
    wrapper.remote = remote

    def piped_remote(**kwargs):
        # import here to avoid cyclic dependencies
        from pysource.transport import do_piped_client_request
        return do_piped_client_request(request_type, kwargs,
                                       sys.stdin, sys.stdout)
    wrapper.piped_remote = piped_remote

    return wrapper


class RequestContext(threading.local):

    def __init__(self):
        super(RequestContext, self).__init__(self)
        self.registered = []
        self.stdin = None
        self.stdout = None

    def add_registered(self, function_holder):
        self.registered.append(function_holder)
request_context = RequestContext()


class RequestContextOut(object):

    @staticmethod
    def write(data):
        request_context.stdout.write(data)
stdout = RequestContextOut()


class RequestContextIn(object):

    @staticmethod
    def read(length=0):
        return request_context.stdin.read(length)
stdin = RequestContextIn()


def function(func=None, piped=False):
    # import here to avoid cyclic dependencies
    from pysource import registry
    if func is not None:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        registry.register(func, wrapper, piped)
        return wrapper
    else:
        def partial_wrapper(fn):
            return function(fn, piped=piped)
        return partial_wrapper


class ExecutionError(argh.CommandError):
    pass
