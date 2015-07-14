#!/usr/bin/env python

import sys
import argparse

from build import BuildManager
from argcommand import Command
from download import DownLoadManager
from port import PortFactory


class DownloadCommand(Command):
    """
    Download a Port
    """

    command_name = 'download'

    def run(self):
        parser = argparse.ArgumentParser(
            description='Download a Port')
        parser.add_argument('portname', nargs='?', help='The Port to download')
        args = parser.parse_args(sys.argv[2:])
        port = PortFactory.loadport(args)
        mgr = DownLoadManager()
        mgr.download(port)


class BuildCommand(Command):
    """
    Build a Port
    """

    command_name = 'build'

    def run(self):
        parser = argparse.ArgumentParser(
            description='Build a Port')
        parser.add_argument('portname', nargs='?', help='The Port to build', default='system/glibc')
        args = parser.parse_args(sys.argv[2:])
        port = PortFactory.loadport(args)
        # mgr = DownLoadManager()
        # mgr.download(port)
        # mgr.extract(port)
        builder = BuildManager()
        builder.build(port)


class InstallCommand(Command):
    """
    Install a Port
    """

    command_name = 'install'

    def run(self):
        print("installing")


class PortCommand(Command):
    """
    The Unix Port System Reborn
    """

    subcommands = [BuildCommand, DownloadCommand, InstallCommand]

    def run(self):
        pass


if "__main__" == __name__:
    PortCommand.execute(['build'])
