import argh

def main(daemon=False):
    if daemon:
        print 'deamon'
    else:
        print 'not daemon'

if __name__ == '__main__':
    argh.dispatch_command(main, completion=False)
