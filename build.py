from yapsy.PluginManager import PluginManager
from yapsy.IPlugin import IPlugin
from abc import abstractmethod
import logging


class BuildManager(object):
    @staticmethod
    def build(port):
        manager = PluginManager()
        manager.setPluginPlaces(["plugins", "~/.ports/plugins"])
        manager.setCategoriesFilter({
            "Build": IBuildPlugin,
            "Configure": IConfigurePlugin
        })
        manager.collectPlugins()


        # Loop through all known configure Plugins We only should ever have one but we don't know which one
        for plugin in manager.getPluginsOfCategory('Configure'):
            plugin.plugin_object.main(port)

        # Same for the build plugins
        for plugin in manager.getPluginsOfCategory('Build'):
            plugin.plugin_object.main(port)


class IBuildPlugin(IPlugin):
    def __init__(self):
        super(IBuildPlugin, self).__init__()
        self.does_apply = False

    @abstractmethod
    def check(self):
        pass

    @abstractmethod
    def run(self):
        pass

    def main(self, port):
        self.port = port
        self.check()
        if self.does_apply:
            logging.info('Building Port {PORTNAME}'.format(PORTNAME=port.portname))
            self.run()


class IConfigurePlugin(IPlugin):
    def __init__(self):
        super(IConfigurePlugin, self).__init__()
        self.does_apply = False

    @abstractmethod
    def configure(self):
        pass

    @abstractmethod
    def check(self):
        pass

    def ask(self):
        pass

    def main(self, port):
        self.port = port
        self.check()
        if self.does_apply:
            self.ask()
            logging.info('Running configuration scripts for {PORTNAME}'.format(PORTNAME=port.portname))
            self.configure()
