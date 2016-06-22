from yapsy.IPlugin import IPlugin
from abc import abstractmethod
from dialog import Dialog
import logging


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
            # Loop through all known configure Plugins We only should ever have one but we don't know which one
            for plugin in self.manager.getPluginsOfCategory('Configuration'):
                if not hasattr(port, 'configuration_plugin'):
                    plugin.plugin_object.main(port)


class IBuildPlugin(IPlugin):
    def __init__(self):
        super(IBuildPlugin, self).__init__()
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
            self.port.is_built = True


class IConfigurePlugin(IPlugin):
    def __init__(self):
        super(IConfigurePlugin, self).__init__()
        self.does_apply = False
        self.port = None

    envclean = 'env -u LD_LIBRARY_PATH'

    @abstractmethod
    def configure(self):
        pass

    @abstractmethod
    def check(self):
        pass

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
        self.port = port
        self.check()
        if self.does_apply:
            self.ask()
            self.configure()
            self.port.is_configured = True
