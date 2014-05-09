from pysource import arguments


class FunctionHolder(object):

    def __init__(self, function, wrapper):
        self.function = function
        self.wrapper = wrapper
        self.type_spec = arguments.ArgTypeSpec(function)
        self.name = function.__name__


registered = {}



def register(function, wrapper):
    holder = FunctionHolder(function, wrapper)
    registered[holder.name] = holder
    print 'registered'
