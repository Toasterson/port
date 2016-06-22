from build import IConfigurePlugin
from prefix import Prefix
import os
import subprocess
import logging


class DotConfigure(IConfigurePlugin):
    def __init__(self):
        super().__init__()
        self.pluginname = 'Dot Configure'
        self.filename = 'configure'

    def configure(self):
        cmd = self.envclean + ' '
        cmd += self.port.sources_root() + '/' + self.filename + ' '
        cmd += '--prefix=' + Prefix.print() + ' '
        cmd += self.get_config_options()
        logging.debug("Running {0}".format(cmd))
        subprocess.call(cmd.split(' '))
