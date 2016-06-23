from yapsy.PluginManager import PluginManager
from yapsy.IPlugin import IPlugin
from abc import abstractmethod
from prefix import Prefix
import logging
import os


class InstallManager(object):
    def __init__(self, manager):
        self.manager = manager

    def install(self, port):

        logging.debug('Installing Port {PORTNAME} into {PREFIX}'.format(PORTNAME=port.portname, PREFIX=Prefix.print()))

        if not hasattr(port, 'is_installed'):
            # Same for the build plugins
            for plugin in self.manager.getPluginsOfCategory('Installing'):
                plugin.plugin_object.main(port)


class IInstallPlugin(IPlugin):

    def __init__(self):
        super(IInstallPlugin, self).__init__()
        self.does_apply = False
        self.port = None
        self.savedPath = None
        self.filename = None
        self.build_bits = ['32', '64']

    def check(self):
        if os.path.exists(os.path.join(getattr(self.port, 'build_dir_64'), self.filename)) or os.path.exists(
                os.path.join(getattr(self.port, 'build_dir_32'), self.filename)):
            self.does_apply = True

    @abstractmethod
    def run(self):
        pass

    def getConfigureOptionsEnvironment(self):
        string = ""
        for key, value in self.port.getEnvironmentOptions().items():
            string += " {0}={1}".format(key, value)
        return string

    def main(self, port):
        self.port = port
        self.check()
        if self.does_apply:
            for bits in self.build_bits:
                try:
                    self.savedPath = os.getcwd()
                    os.chdir(getattr(self.port, 'build_dir_{0}'.format(bits)))
                except:
                    raise Exception("Error: port source dir {0} does not exist".format(self.port.build_dir))
                self.port.updateEnvironmentVariable('BITS', bits)
                self.run()
            self.port.is_built = True
            os.chdir(self.savedPath)
