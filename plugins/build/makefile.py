from build import IBuildPlugin
import os
import subprocess


class Makefile(IBuildPlugin):
    def check(self):
        for dir, subdirs, files in os.walk(self.port.sources_root()):
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
            os.chdir(self.port.source_dir)
        except:
            print("Error: invalid path {0} Exiting".format(self.port.source_dir))
            exit(1)
        print("Running {0}".format(cmd))
        subprocess.call(cmd.split(' '))
