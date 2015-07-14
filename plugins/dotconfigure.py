from build import IConfigurePlugin

import os


class DotConfigure(IConfigurePlugin):
    def check(self):
        for dir, subdirs, files in os.walk(self.port.sources_root()):
            for f in files:
                if f == 'configure':
                    self.does_apply = True
                    self.port.source_dir = dir
                    self.port.confguration_plugin = 'Dot Configure'
                    return

    def configure(self):
        pass
