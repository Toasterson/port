import os
import io
import sys
import logging
from yaml import load, dump

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


# TODO move default values from __init__ to config
class Port(object):
    def __init__(self, portname):
        # TODO make function to transform fullpath to portname
        self.portname = portname
        self.version = ''
        self.name = ''
        self.sources_root_scheme = '~/.ports/cache/{PORTNAME}/src'
        self.download_dir_scheme = '~/.ports/cache/{PORTNAME}/downloads'
        self.filename_scheme = '{PORTNAME}-{VERSION}.tar.gz'

    def sources_root(self):
        return os.path.expanduser(
            self.sources_root_scheme.format(PORTNAME=self.portname))

    def download_dir(self):
        return os.path.expanduser(
            self.download_dir_scheme.format(PORTNAME=self.portname))

    def download_filename(self):
        return os.path.expanduser(
            self.download_dir_scheme.format(PORTNAME=self.portname) + '/' + self.filename_scheme.format(
                PORTNAME=self.portname, VERSION=self.version)
        )


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
        for dir, subdirs, files in walk_up(os.path.join(root, port.portname), root):
            for f in files:
                if f == 'port.yaml' or f == '{0}.yaml'.format(sys.platform):
                    logging.info('Loading port metadata from {0}'.format(f))
                    with io.open(os.path.join(dir, f), 'r') as port_desc:
                        port.__dict__.update(load(port_desc, Loader=Loader))
        if port.name == '':
            print('ERROR:Port {PORTNAME} could not be loaded'.format(PORTNAME=port.portname))
            sys.exit(1)
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
