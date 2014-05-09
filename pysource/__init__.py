import functools


from pysource import registry


def function(func, *args, **kwargs):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    registry.register(func, wrapper)
    return wrapper

