from yapsy.IPlugin import IPlugin
from abc import abstractmethod
from dialog import Dialog
import logging
import shutil
import os


def make_build_dirs(port):
    for bits in ['32', '64']:
        build_dir = os.path.join(port.build_root(), bits)
        setattr(port, 'build_dir_{0}'.format(bits), build_dir)
        if os.path.exists(build_dir):
            shutil.rmtree(build_dir)
        os.makedirs(build_dir)


class BuildManager(object):
    def __init__(self, manager):
        self.manager = manager

    def build(self, port):

        logging.debug('Building Port {0}'.format(port.portname))

        if not hasattr(port, 'is_built'):
            # Same for the build plugins
            for plugin in self.manager.getPluginsOfCategory('Building'):
                if not hasattr(port, 'build_plugin'):
                    plugin.plugin_object.main(port)

    def configure(self, port):
        logging.debug('Configuring Build for {0}'.format(port.portname))
        if not hasattr(port, 'is_configured'):
            make_build_dirs(port)
            # Loop through all known configure Plugins We only should ever have one but we don't know which one
            for plugin in self.manager.getPluginsOfCategory('Configuration'):
                if not hasattr(port, 'configuration_plugin'):
                    plugin.plugin_object.main(port)


class IBuildPlugin(IPlugin):
    def __init__(self):
        super(IBuildPlugin, self).__init__()
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


class IConfigurePlugin(IPlugin):
    def __init__(self):
        super(IConfigurePlugin, self).__init__()
        self.pluginname = None
        self.filename = None
        self.does_apply = False
        self.port = None
        self.savedPath = None
        self.build_bits = ['32', '64']

    @abstractmethod
    def configure(self):
        pass

    def check(self):
        if os.path.exists(os.path.join(self.port.sources_root(), self.filename)):
            self.does_apply = True

    def getConfigureOptionsEnvironment(self):
        string = ""
        for key, value in self.port.getEnvironmentOptions().items():
            string += " {0}={1}".format(key, value)
        return string

    def ask(self):
        if hasattr(self.port, 'config'):
            dialog = Dialog(dialog='dialog')
            dialog.set_background_title('Conguration for {PORTNAME}'.format(PORTNAME=self.port.portname))
            portchoices = []
            for option, optvalues in self.port.config.items():
                self.port.config[option]['user_choice'] = False
                portchoices.append((option, optvalues['description'], optvalues['default']))
            code, tags = dialog.checklist(
                'Choose your Configuration for {PORTNAME}'.format(PORTNAME=self.port.portname),
                choices=portchoices, title="Port configuration")
            if code == dialog.OK:
                for tag in tags:
                    self.port.config[tag]['user_choice'] = True
            print('\n')

    def main(self, port):
        # TODO make configuration options that are preset in port.yaml and can be modified via commandline
        # TODO make environement controlled
        # TODO i86 and amd64 dual build
        self.port = port
        self.check()
        if self.does_apply:
            self.ask()
            for bits in self.build_bits:
                try:
                    self.savedPath = os.getcwd()
                    os.chdir(getattr(self.port, 'build_dir_{0}'.format(bits)))
                except:
                    raise Exception("Error: port source dir {0} does not exist".format(self.port.build_dir))
                self.port.updateEnvironmentVariable('BITS', bits)
                self.configure()
            self.port.is_configured = True
            os.chdir(self.savedPath)
            self.port.configuration_plugin = self.pluginname

    def get_config_options(self):
        string = ''
        if hasattr(self.port, 'config'):
            for option, optvalue in self.port.config.items():
                if optvalue['user_choice']:
                    if optvalue['enabled'] != '':
                        string += ' ' + optvalue['enabled']
                else:
                    if optvalue['disabled'] != '':
                        string += ' ' + optvalue['disabled']
        return string
