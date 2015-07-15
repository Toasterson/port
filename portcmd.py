#!/usr/bin/env python

import os
import logging

from build import BuildManager
from argcommand import Command
from argcommand import Argument
from download import DownLoadManager
from port import PortFactory
import locale


class DownloadCommand(Command):
    """
    Download a Port
    """

    command_name = 'download'
    portname = Argument('portname', nargs='?', help='The Port to download', default=os.path.realpath(os.curdir))

    def run(self):
        port = PortFactory.loadport(self)
        mgr = DownLoadManager()
        mgr.download(port)


class BuildCommand(Command):
    """
    Build a Port
    """

    command_name = 'build'
    portname = Argument('portname', nargs='?', help='The Port to download', default=os.path.realpath(os.curdir))

    def run(self):
        port = PortFactory.loadport(self)
        # mgr = DownLoadManager()
        # mgr.download(port)
        # mgr.extract(port)
        BuildManager.build(port)


class InstallCommand(Command):
    """
    Install a Port
    """

    command_name = 'install'
    portname = Argument('portname', nargs='?', help='The Port to download', default=os.path.realpath(os.curdir))

    def run(self):
        print("installing")


class PortCommand(Command):
    """
    The Unix Port System Reborn
    """

    subcommands = [BuildCommand, DownloadCommand, InstallCommand]

    loglevel = Argument('--log', help='Set Logging level', dest='loglevel')

    def run(self):
        numeric_level = getattr(logging, self.loglevel.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % self.loglevel)
        logging.basicConfig(level=numeric_level)


if "__main__" == __name__:
    locale.setlocale(locale.LC_ALL, '')
    PortCommand.execute(['build', 'system/glibc'])
