#!/usr/bin/env python

import os
from build import BuildManager, IBuildPlugin, IConfigurePlugin
import argparse
from download import DownLoadManager
from port import PortFactory
import locale
from install import InstallManager, IInstallPlugin
from yapsy.PluginManager import PluginManager

class PortCmd:
    """
    The Unix Port System Reborn
    """

    def __init__(self):
        self.manager = PluginManager()
        self.manager.setPluginPlaces([
            "plugins/building", "~/.ports/plugins/building",
            "plugins/configuration", "~/.ports/plugins/configuration",
            "plugins/installing", "~/.ports/plugins/installing"
        ])
        self.manager.setCategoriesFilter({
            'Building': IBuildPlugin,
            'Configuration': IConfigurePlugin,
            'Installing': IInstallPlugin
        })
        self.manager.collectPlugins()

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
        args = parser.parse_args(['install'])
        self.args = ['runtime/python3']
        # args = parser.parse_args(sys.argv[1:2])
        # self.args = sys.argv[2:]
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()
        # Todo Save Information of Port into file in cache

    def download(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('portname', nargs='?', help='Name of the Port', default=os.path.realpath(os.curdir))
        port = PortFactory.loadport(parser.parse_args(self.args))
        DownLoadManager.download(port)

    def build(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('portname', nargs='?', help='Name of the Port', default=os.path.realpath(os.curdir))
        port = PortFactory.loadport(parser.parse_args(self.args))
        DownLoadManager.download(port)
        DownLoadManager.extract(port)
        buildman = BuildManager(self.manager)
        buildman.configure(port)
        buildman.build(port)

    def install(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('portname', nargs='?', help='Name of the Port', default=os.path.realpath(os.curdir))
        port = PortFactory.loadport(parser.parse_args(self.args))
        DownLoadManager.download(port)
        DownLoadManager.extract(port)
        buildman = BuildManager(self.manager)
        buildman.configure(port)
        buildman.build(port)
        instman = InstallManager(self.manager)
        instman.install(port)


if "__main__" == __name__:
    locale.setlocale(locale.LC_ALL, '')
    PortCmd()
