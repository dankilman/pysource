import sys

import argh

from pysource import daemonizer

def daemon(action):
    if action == 'start':
        daemonizer.start()
    elif action == 'stop':
        daemonizer.stop()
    else:
        raise argh.CommandError('unreconized action: {0} '
                                '[valid: start, stop]'.format(action))


def source(source_path):
    pass


def run(function_name, *args):
    print function_name, args


def main():
    argh.dispatch_commands([
        daemon,
        source,
        run
    ], completion=False)


if __name__ == '__main__':
    main()
