import os
import io
from yaml import load, dump

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


class Port(object):
    def __init__(self):
        self.version = ''
        self.name = ''
        self.base_url = ''
        self.source_dir_scheme = '~/.ports_cache/{NAME}/src'
        self.download_dir_scheme = '~/.ports_cache/{NAME}/downloads'
        self.filename = '{NAME}-{VERSION}.{SUFFIX}'
        self.url_scheme = '{BASEURL}/{NAME}-{VERSION}.{SUFFIX}'
        self.suffix = 'tar.gz'

    def download_url(self):
        return self.url_scheme.format(BASEURL=self.base_url, NAME=self.name, VERSION=self.version, SUFFIX=self.suffix)

    def source_dir(self):
        return os.path.expanduser(self.source_dir_scheme.format(VERSION=self.version, NAME=self.name))

    def download_dir(self):
        return os.path.expanduser(self.download_dir_scheme.format(VERSION=self.version, NAME=self.name))

    def download_filename(self):
        return os.path.join(self.download_dir(),
                            self.filename.format(VERSION=self.version, NAME=self.name, SUFFIX=self.suffix))


class PortFactory(object):
    @staticmethod
    def loadport(portname):
        port = Port()
        with io.open(os.path.abspath(os.path.join('/usr/ports', portname, 'port.yaml')),
                     'r') as port_desc:
            loadedport = load(port_desc)
            port.__dict__.update(loadedport)
        return port
