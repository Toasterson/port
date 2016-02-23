from yapsy.PluginManager import PluginManager
from yapsy.IPlugin import IPlugin
from abc import abstractmethod
from prefix import Prefix


class InstallManager(object):
    def __init__(self, manager):
        self.manager = manager

    def install(self, port):

        print('Installing Port {PORTNAME} into {PREFIX}'.format(PORTNAME=port.portname, PREFIX=Prefix.print()))

        if not hasattr(port, 'is_installed'):
            # Same for the build plugins
            for plugin in self.manager.getPluginsOfCategory('Installing'):
                plugin.plugin_object.main(port)


class IInstallPlugin(IPlugin):
    def __init__(self):
        super(IInstallPlugin, self).__init__()
        self.does_apply = False
        self.port = None

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
            self.run()
            self.port.is_installed = True
