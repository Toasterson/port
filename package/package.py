
class Package(object):

    def __init__(self, portsdir):
        self.portsdir = portsdir
        self.load()

    def load(self):
        self.version = 1

    def __repr__(self):
        return 'Loading Port from {portsdir}'.format(portsdir=self.portsdir)