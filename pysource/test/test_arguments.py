from unittest import TestCase

from pysource.arguments import ArgTypeSpec


class ArgumentsTest(TestCase):

    def _assert_valid_parsing(self, fun, args, expected_parsed_args):
        self.assertEqual(ArgTypeSpec(fun).parse(args),
                         expected_parsed_args)

    def test_plain_args(self):
        def fun(arg1):
            pass
        self._assert_valid_parsing(fun, ['1'], ['1'])

    def test_typed_args(self):
        def fun(arg1=int, arg2=float, arg3=str):
            pass
        self._assert_valid_parsing(fun, ['1', '2.2', '3'], [1, 2.2, '3'])

    def test_mixed_args(self):
        def fun(arg1, arg2=int):
            pass
        self._assert_valid_parsing(fun, ['1', '2'], ['1', 2])
