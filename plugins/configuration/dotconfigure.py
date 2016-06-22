from build import IConfigurePlugin
from prefix import Prefix
import subprocess
import logging


class DotConfigure(IConfigurePlugin):
    def __init__(self):
        super().__init__()
        self.pluginname = 'Dot Configure'
        self.filename = 'configure'

    def configure(self):
        cmd = self.port.sources_root() + '/' + self.filename + ' '
        cmd += '--prefix=' + Prefix.print() + ' '
        cmd += self.get_config_options()
        cmd += self.getConfigureOptionsEnvironment()
        logging.debug("Running {0}".format(cmd))
        subprocess.call(cmd.split(' '), env=self.port.getEnvironment())
