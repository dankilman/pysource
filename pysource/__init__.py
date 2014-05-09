import functools
import threading
import uuid

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
