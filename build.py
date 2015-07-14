from yapsy.PluginManager import PluginManager
from yapsy.IPlugin import IPlugin


class BuildManager(object):
    def build(self, port):
        manager = PluginManager()
        manager.setPluginPlaces(["plugins", "~/.ports/plugins"])
        manager.setCategoriesFilter({
            "Build": IBuildPlugin,
        })
        manager.collectPlugins()

        # Loop round the plugins and print their names.
        for plugin in manager.getAllPlugins():
            plugin.plugin_object.build()


class IBuildPlugin(IPlugin):
    def build(self):
        pass
