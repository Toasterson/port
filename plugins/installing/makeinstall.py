from install import IInstallPlugin
import logging
import subprocess


class MakeInstall(IInstallPlugin):

    def __init__(self):
        super().__init__()
        self.filename = 'Makefile'

    def run(self):
        cmd = 'make install'
        logging.debug("Running {0} in {1}".format(cmd, getattr(self.port, 'build_dir_{0}'.format(
            self.port.getEnvironmentVariable('BITS')))))
        subprocess.call(cmd.split(' '), env=self.port.getEnvironment())
