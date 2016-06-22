from build import IBuildPlugin
import os
import subprocess
import logging


# TODO i86 and amd64 dual build
class Makefile(IBuildPlugin):
    def __init__(self):
        super().__init__()
        self.savedPath = None

    def check(self):
        for dir, subdirs, files in os.walk(self.port.build_dir):
            for f in files:
                if f == 'Makefile':
                    self.does_apply = True
                    self.port.source_dir = dir
                    self.port.build_plugin = 'Makefile'
                    return

    def run(self):
        cmd = 'make'
        try:
            self.savedPath = os.getcwd()
            os.chdir(self.port.build_dir)
        except:
            raise Exception("Error: build dir path {0} does not exist".format(self.port.build_dir))

        logging.debug("Running {0} in {1}".format(cmd, self.port.build_dir))
        subprocess.call(cmd)
        os.chdir(self.savedPath)
