from build import IBuildPlugin


class PluginOne(IBuildPlugin):
    def build(self):
        print "This is plugin 1"
