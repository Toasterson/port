from build import IConfigurePlugin
from prefix import Prefix
import subprocess
import logging


class AutogenSh(IConfigurePlugin):
    def __init__(self):
        super().__init__()
        self.pluginname = 'Autogen.sh'
        self.filename = 'autogen.sh'

    def configure(self):
        cmd = self.envclean + ' '
        cmd += self.port.sources_root() + '/' + self.filename + ' '
        cmd += '--prefix=' + Prefix.print() + ' '
        cmd += self.get_config_options()
        logging.debug("Running {0}".format(cmd))
        subprocess.call(cmd.split(' '))
