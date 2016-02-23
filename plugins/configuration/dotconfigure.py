from build import IConfigurePlugin
from prefix import Prefix
import os
import subprocess
import shutil


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
        cmd = self.envclean + ' '
        if 'seperate_build_dir' in self.port.__dict__:
            # Todo Use Port Source Dir instead of assuming build dir is subdir of source dir
            cmd += '../configure '
        else:
            cmd += './configure '
        cmd += '--prefix=' + Prefix.print() + ' '

        for option, optvalue in self.port.config.items():
            if optvalue['user_choice']:
                if optvalue['enabled'] != '':
                    cmd = cmd + ' ' + optvalue['enabled']
            else:
                if optvalue['disabled'] != '':
                    cmd = cmd + ' ' + optvalue['disabled']

        try:
            self.savedPath = os.getcwd()
            os.chdir(self.port.source_dir)
        except:
            print("Error: invalid path {0} Exiting".format(self.port.source_dir))
            exit(1)

        if 'seperate_build_dir' in self.port.__dict__:
            build_dir = os.path.join(self.port.source_dir, 'build')
            if os.path.exists(build_dir):
                shutil.rmtree(build_dir)
            os.makedirs(build_dir)
            try:
                self.savedPath = os.getcwd()
                os.chdir(build_dir)
            except:
                print("Error: invalid path {0} Exiting".format(build_dir))
                exit(1)
        print("Running {0}".format(cmd))
        subprocess.call(cmd.split(' '))
