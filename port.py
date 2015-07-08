#!/usr/bin/env python

from argcommand import Command
from argcommand import Argument
from yapsy.PluginManager import PluginManager
from portbuild.cmd import BuildCommand
from download.cmd import DownloadCommand
from install.cmd import InstallCommand


class Port(Command):
    """
    The Unix Port System Reborn
    """

    subcommands = [BuildCommand, DownloadCommand, InstallCommand]

    def run( self ):
        pass


if "__main__" == __name__:
    Port.execute()
