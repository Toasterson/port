import os
import io
import sys
import logging
from yaml import load, dump
from environment import EnvironmentManager

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def get_platform():
    return sys.platform


# TODO move default values from __init__ to config
class Port(object):
    def __init__(self, portname):
        # TODO make function to transform fullpath to portname
        self.portname = portname
        self.platform = get_platform()
        self.version = ''
        self.name = ''
        self.default_version = {}
        self.sources_root_scheme = '~/.ports/cache/{PORTNAME}/src'
        self.download_dir_scheme = '~/.ports/cache/{PORTNAME}/downloads'
        self.build_dir_scheme = '~/.ports/cache/{PORTNAME}/build'
        self.filename_scheme = '{PORTNAME}-{VERSION}.tar.gz'
        self.environment = {}
        self.env = EnvironmentManager()

    def get_default_version(self):
        return self.default_version.get(get_platform())

    def sources_root(self):
        return os.path.expanduser(self.sources_root_scheme.format(PORTNAME=self.portname))

    def download_dir(self):
        return os.path.expanduser(self.download_dir_scheme.format(PORTNAME=self.portname))

    def download_filename(self):
        return os.path.expanduser(
            self.download_dir_scheme.format(PORTNAME=self.portname) + '/' + self.filename_scheme.format(
                PORTNAME=self.portname, VERSION=self.version)
        )

    def build_root(self):
        return os.path.expanduser(self.build_dir_scheme.format(PORTNAME=self.portname))

    def getEnvironment(self):
        return self.env.getEnvironment()

    def getEnvironmentVariable(self, key):
        return self.env.getVariable(key)

    def getEnvironmentOptions(self):
        return self.env.getOptions()

    def updateEnvironmentVariable(self, key, value):
        self.env.updateVariable(key, value)


class PortFactory(object):
    @staticmethod
    def loadport(args):
        '''
        Parses all Config Parameters passed via args and loads all Parameters in the Yaml Files
        Returns the Flattened Config as an Instance of the Python class Port
        :param args:
        :return: port:
        '''
        port = Port(args.portname)
        # TODO move this to config.yaml and make functions to load the Config
        root = './portstree'
        portsfile = os.path.join(root, port.portname, 'port.yaml')
        logging.info('Loading port metadata for {0} from {1}'.format(port.portname, portsfile))
        with io.open(portsfile, 'r') as port_desc:
            port.__dict__.update(load(port_desc, Loader=Loader))

        if port.name == '':
            raise Exception('ERROR:Port {0} could not be loaded'.format(port.portname))

        envfile = os.path.join(root, '{0}.yaml'.format(port.platform))
        with io.open(envfile, 'r') as env_desc:
            logging.info('Loading environment variables for {0} from {1}'.format(port.portname, envfile))
            port.env.loadEnvironment(load(env_desc, Loader=Loader))

        if hasattr(port, 'environment'):
            port.env.loadEnvironment(port.environment)
            del port.environment
        # TODO load dependency metadata here
        return port


# TODO move to util.py
def walk_up(bottom, top):
    """
    mimic os.walk, but walk 'up'
    instead of down the directory tree
    """

    bottom = os.path.realpath(bottom)
    top = os.path.realpath(top)

    # get files in current dir
    try:
        names = os.listdir(bottom)
    except Exception as e:
        print(e)
        return

    dirs, nondirs = [], []
    for name in names:
        if os.path.isdir(os.path.join(bottom, name)):
            dirs.append(name)
        else:
            nondirs.append(name)

    yield bottom, dirs, nondirs

    new_path = os.path.realpath(os.path.join(bottom, '..'))

    # see if we are at the top
    if new_path == top:
        return

    for x in walk_up(new_path, top):
        yield x
