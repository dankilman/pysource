

def create_shell_functions(function_names):
    return ''.join([_create_shell_function(name)
                   for name in function_names])


def _create_shell_function(function_name):
    return '''%(function_name)s()
{
    __pysource_run %(function_name)s $@
}

''' % dict(function_name=function_name)
