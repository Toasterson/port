#!/usr/bin/env python

import argparse
import sys
import os
from package import Package

class Port(object):
    def __init__(self):
        parser = argparse.ArgumentParser(
            description='The Unix Port System Reborn',
            usage='''port <command> [<args>]

The following commands are available:
   download     download a port
   build        build a port but do not install
''')
        parser.add_argument('command', help='Subcommand to run')
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print 'Unrecognized command'
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    def download(self):
        parser = argparse.ArgumentParser(
            description='download a port')
        # prefixing the argument with -- means it's optional
        parser.add_argument('port', nargs='?', default=os.getcwd())
        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (port) and the subcommand (download)
        args = parser.parse_args(sys.argv[2:])
        pkg = Package(args.port)
        print pkg

    def build(self):
        parser = argparse.ArgumentParser(
            description='build a port but do not install')
        parser.add_argument('port', nargs='?', default=os.getcwd())
        args = parser.parse_args(sys.argv[2:])



if __name__ == '__main__':
    Port()