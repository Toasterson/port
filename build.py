from yapsy.PluginManager import PluginManager
from yapsy.IPlugin import IPlugin
from abc import abstractmethod
from dialog import Dialog


class BuildManager(object):
    @staticmethod
    def build(port):
        manager = PluginManager()
        manager.setPluginPlaces(["plugins", "~/.ports/plugins"])
        manager.setCategoriesFilter({
            "Build": IBuildPlugin
        })
        manager.collectPlugins()

        print('Building Port {PORTNAME}'.format(PORTNAME=port.portname))

        # Same for the build plugins
        for plugin in manager.getPluginsOfCategory('Build'):
            plugin.plugin_object.main(port)

    @staticmethod
    def configure(port):
        manager = PluginManager()
        manager.setPluginPlaces(["plugins", "~/.ports/plugins"])
        manager.setCategoriesFilter({
            "Configure": IConfigurePlugin
        })
        manager.collectPlugins()

        print('Configuring Build for {PORTNAME}'.format(PORTNAME=port.portname))

        # Loop through all known configure Plugins We only should ever have one but we don't know which one
        for plugin in manager.getPluginsOfCategory('Configure'):
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


class IConfigurePlugin(IPlugin):
    def __init__(self):
        super(IConfigurePlugin, self).__init__()
        self.does_apply = False

    envclean = 'env -u LD_LIBRARY_PATH '

    @abstractmethod
    def configure(self):
        pass

    @abstractmethod
    def check(self):
        pass

    def ask(self):
        dialog = Dialog(dialog='dialog')
        dialog.set_background_title('Conguration for {PORTNAME}'.format(PORTNAME=self.port.portname))
        portchoices = []
        for option, optvalues in self.port.config.items():
            self.port.config[option]['user_choice'] = False
            portchoices.append((option, optvalues['description'], optvalues['default']))
        code, tags = dialog.checklist('Choose your Configuration for {PORTNAME}'.format(PORTNAME=self.port.portname),
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
