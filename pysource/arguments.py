from argh.utils import get_arg_spec


class ArgTypeSpec(object):

    def __init__(self, function):
        self.function_name = function.__name__
        spec = get_arg_spec(function)
        args_len = len(spec.args)
        defaults = spec.defaults or []
        if len(defaults) < args_len:
            prefix = [str for _ in range(args_len - len(defaults))]
            defaults = prefix + list(defaults)
        self.types = defaults

    def parse(self, args):
        if len(args) != len(self.types):
            raise RuntimeError(
                '{0}() takes exactly {1} arguments ({2} given)'
                .format(self.function_name, len(self.types), len(args)))

        return [tpe(arg) for (tpe, arg) in zip(self.types, args)]
