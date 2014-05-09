from pysource import arguments


class FunctionHolder(object):

    def __init__(self, function, wrapper):
        self.function = function
        self.wrapper = wrapper
        self.type_spec = arguments.ArgTypeSpec(function)
        self.name = function.__name__

    def run(self, args):
        parsed_args = self.type_spec.parse(args)
        return self.wrapper(*parsed_args)


registered = {}


def register(function, wrapper, request_context=None):
    holder = FunctionHolder(function, wrapper)
    registered[holder.name] = holder
    if request_context is not None:
        request_context.add_registered(holder)


def run_function(function_name, args):
    return registered[function_name].run(args)
