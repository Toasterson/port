from yapsy.PluginManager import PluginManager
from yapsy.IPlugin import IPlugin
from abc import abstractmethod
from dialog import Dialog


class BuildManager(object):
    def __init__(self):
        self.manager = PluginManager()
        self.manager.setPluginPlaces([
            "plugins/building", "~/.ports/plugins/building",
            "plugins/configuration", "~/.ports/plugins/configuration"
        ])
        self.manager.setCategoriesFilter({
            'Building': IBuildPlugin,
            'Configuration': IConfigurePlugin
        })
        self.manager.collectPlugins()

    def build(self, port):

        print('Building Port {PORTNAME}'.format(PORTNAME=port.portname))

        if not port.is_built:
            # Same for the build plugins
            for plugin in self.manager.getPluginsOfCategory('Building'):
                plugin.plugin_object.main(port)

    def configure(self, port):
        print('Configuring Build for {PORTNAME}'.format(PORTNAME=port.portname))

        if not port.is_configured:
            # Loop through all known configure Plugins We only should ever have one but we don't know which one
            for plugin in self.manager.getPluginsOfCategory('Configuration'):
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
        self.port = None

    envclean = 'env -u LD_LIBRARY_PATH'

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
