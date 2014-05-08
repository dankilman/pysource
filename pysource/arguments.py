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


if __name__ == '__main__':

    def fun1(arg1):
        pass

    assert ArgTypeSpec(fun1).parse(['1']) == ['1']

    def fun2(arg1=int, arg2=float, arg3=str):
        pass

    assert ArgTypeSpec(fun2).parse(['1', '2.2', '3']) == [1, 2.2, '3']

    def fun3(arg1, arg2=int):
        pass

    assert ArgTypeSpec(fun3).parse(['1', '2']) == ['1', 2]

