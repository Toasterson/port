import os


class Port(object):
    def __init__(self):
        self.version = '2.21'
        self.name = 'glibc'
        self.base_url = 'https://ftp.gnu.org/gnu/libc'
        self.source_dir_scheme = '~/.ports_cache/{NAME}/src'
        self.download_dir_scheme = '~/.ports_cache/{NAME}/downloads'
        self.filename = '{NAME}-{VERSION}.{SUFFIX}'
        self.url_scheme = '{BASEURL}/{NAME}-{VERSION}.{SUFFIX}'
        self.suffix = 'tar.xz'

    def download_url(self):
        return self.url_scheme.format(BASEURL=self.base_url, NAME=self.name, VERSION=self.version, SUFFIX=self.suffix)

    def source_dir(self):
        return os.path.expanduser(self.source_dir_scheme.format(VERSION=self.version, NAME=self.name))

    def download_dir(self):
        return os.path.expanduser(self.download_dir_scheme.format(VERSION=self.version, NAME=self.name))

    def download_filename(self):
        return os.path.join(self.download_dir(),
                            self.filename.format(VERSION=self.version, NAME=self.name, SUFFIX=self.suffix))
