from argh.utils import get_arg_spec


class ArgTypeSpec(object):

    def __init__(self, function):
        spec = get_arg_spec(function)
        args_len = len(spec.args)
        defaults = spec.defaults or []
        if len(defaults) < args_len:
            prefix = [str for _ in range(args_len - len(defaults))]
            defaults = prefix + list(defaults)
        self.types = defaults

    def parse(self, args):
        return [tpe(arg) for (tpe, arg) in zip(self.types, args)]
