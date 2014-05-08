import argh

from pysource import daemonizer

def run(daemon=False, kill_daemon=False):
    if daemon:
        daemonizer.start()
    elif kill_daemon:
        daemonizer.stop()
    else:
        print 'not daemon'


def main():
    argh.dispatch_command(run, completion=False)


if __name__ == '__main__':
    main()