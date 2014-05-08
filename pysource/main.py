import argh

from pysource import daemonizer

def main(daemon=False):
    if daemon:
        daemonizer.start()
    else:
        print 'not daemon'

if __name__ == '__main__':
    argh.dispatch_command(main, completion=False)
