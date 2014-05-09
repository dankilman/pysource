from pysource import function


@function
def fun1(name, name2, name3):
    return 'name: {0}, name2: {1}, name3: {2}'.format(name, name2, name3)


@function
def fun2(name):
    return 'name: {0}'.format(name)


@function
def fun3(name):
    return 'fun3: {0}'.format(name)
