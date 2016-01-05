#!/usr/bin/env python

import os
import logging

from build import BuildManager
import argparse
import sys
from download import DownLoadManager
from port import PortFactory
import locale


class PortCmd:
    """
    The Unix Port System Reborn
    """

    def __init__(self):
        parser = argparse.ArgumentParser(
                description='The Unix Port System Reborn',
                usage='''ports <command> [<args>]

The most commonly used ports commands are:
   download     Download the Port source
   build        Build the Port
   install      Install the Port
''')
        parser.add_argument('command', help='Subcommand to run')
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(['build'])
        self.args = ['system/glibc']
        # args = parser.parse_args(sys.argv[1:2])
        # self.args = sys.argv[2:]
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    def download(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('portname', nargs='?', help='Name of the Port', default=os.path.realpath(os.curdir))
        port = PortFactory.loadport(parser.parse_args(self.args))
        mgr = DownLoadManager()
        mgr.download(port)

    def build(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('portname', nargs='?', help='Name of the Port', default=os.path.realpath(os.curdir))
        port = PortFactory.loadport(parser.parse_args(self.args))
        mgr = DownLoadManager()
        mgr.download(port)
        mgr.extract(port)
        BuildManager.build(port)



        # def install(self):
        #     numeric_level = getattr(logging, self.loglevel.upper(), None)
        #     if not isinstance(numeric_level, int):
        #         raise ValueError('Invalid log level: %s' % self.loglevel)
        #     logging.basicConfig(level=numeric_level)


if "__main__" == __name__:
    locale.setlocale(locale.LC_ALL, '')
    PortCmd()
