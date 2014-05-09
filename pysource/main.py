import argh

from pysource import daemonizer
from pysource import client


def daemon(action):
    if action == 'start':
        daemonizer.start()
    elif action == 'stop':
        daemonizer.stop()
    elif action == 'restart':
        daemonizer.restart()
    else:
        raise argh.CommandError('unrecognized action: {0} '
                                '[valid: start, stop, restart]'.format(action))


def source(source_path):
    return client.source_register(source_path)


def run(function_name, *args):
    return client.run_function(function_name, args)


def main():
    argh.dispatch_commands([
        daemon,
        source,
        run
    ], completion=False)


if __name__ == '__main__':
    main()
