from build import IBuildPlugin
import subprocess
import logging


class Makefile(IBuildPlugin):

    def __init__(self):
        super().__init__()
        self.filename = 'Makefile'

    def run(self):
        cmd = 'make'
        logging.debug("Running {0} in {1}".format(cmd, getattr(self.port, 'build_dir_{0}'.format(
            self.port.getEnvironmentVariable('BITS')))))
        subprocess.call(cmd, env=self.port.getEnvironment())
