from build import IBuildPlugin
import os
import subprocess
import logging


class Makefile(IBuildPlugin):

    def __init__(self):
        super().__init__()
        self.filename = 'Makefile'

    def run(self):
        cmd = 'make'
        logging.debug("Running {0} in {1}".format(cmd, getattr(self.port, 'build_dir_amd64')))
        subprocess.call(cmd)
