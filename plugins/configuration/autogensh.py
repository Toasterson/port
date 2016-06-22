from build import IConfigurePlugin
from prefix import Prefix
from config import ConfigurationManager as cm
import os
import subprocess
import shutil
import logging


class AutogenSh(IConfigurePlugin):
    def __init__(self):
        super().__init__()
        self.savedPath = None

    def check(self):
        for dir, subdirs, files in os.walk(self.port.sources_root()):
            for f in files:
                if f == 'configure':
                    self.does_apply = True
                    self.port.source_dir = dir
                    self.port.configuration_plugin = 'Dot Configure'
                    return

    def configure(self):
        cmd = self.envclean + ' '
        cmd += self.port.sources_root() + '/configure' + ' '
        cmd += '--prefix=' + Prefix.print() + ' '
        # TODO Refactor out
        if hasattr(self.port, 'config'):
            for option, optvalue in self.port.config.items():
                if optvalue['user_choice']:
                    if optvalue['enabled'] != '':
                        cmd = cmd + ' ' + optvalue['enabled']
                else:
                    if optvalue['disabled'] != '':
                        cmd = cmd + ' ' + optvalue['disabled']

        logging.debug("Running {0}".format(cmd))
        subprocess.call(cmd.split(' '))
        os.chdir(self.savedPath)
