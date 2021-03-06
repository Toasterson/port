import os
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from dialog import Dialog
import zlib
import patoolib
import shutil
import hglib
import logging

# Download URLs in chunks of 256 kB.
CHUNK_SIZE = 256 * 1024


def filter_versions(version):
    version_string = version[0].decode()
    if version_string == 'tip':
        return False
    for value in ['rc', 'a', 'b', 'c']:
        head, sep, tail = version_string.partition(value)
        if sep != '' and tail != '':
            return False
    return True


def ask_version(versions, port):
    versions = list(filter(filter_versions, versions))
    dialog = Dialog(dialog='dialog')
    dialog.set_background_title('Choose version for {PORTNAME}'.format(PORTNAME=port.portname))
    choices = []
    for version in versions:
        if type(version) == tuple:
            ver = version[0]
        else:
            ver = version

        if type(ver) == bytes:
            choices.append((ver.decode(), "", False))
        else:
            choices.append((ver, "", False))
    choices = sorted(choices, key=lambda v: v[0])
    choices.append((choices.pop()[0], "", True))
    choices = list(reversed(choices))
    code, tag = dialog.radiolist(
        'Choose version for {PORTNAME}'.format(PORTNAME=port.portname),
        choices=choices, title="Choose Version")
    if code == dialog.OK:
        return tag
    elif code == dialog.CANCEL:
        return port.get_default_version()


class DownLoadManager(object):
    def __init__(self, manager):
        self.manager = manager

    def hg_get(self, port):
        if not os.path.exists(port.sources_root() + '/.hg'):
            logging.debug('Cloning Mercurial repository {0} into {1}'.format(port.portname, port.sources_root()))
            hglib.clone(port.source.get('hg'), port.sources_root())
        else:
            logging.debug('Using existing repository in {0}'.format(port.sources_root()))
        client = hglib.open(port.sources_root())
        version = ask_version(client.tags(), port)
        if version is None:
            raise Exception('No version selected and no default version found')
        logging.debug('Version {0} was selected'.format(version))
        client.update(version.encode())
        logging.debug('Source is now at Version {0}'.format(version))
        port.version = version

    def git_get(self, port):
        pass

    def svn_get(self, port):
        pass

    def file_get(self, port):
        versions = []
        for version in port.source.file:
            versions.append(version)
        ask_version(versions, port)
        self.download_file(port)

    def download_file(self, port):
        # create download cache if needed
        if not os.path.exists(port.download_dir()):
            os.makedirs(port.download_dir())

        # Download URL.
        url_handle = None
        try:
            request = Request(url=port.download_url())

            # if file already exists, add some headers to the request
            # so we don't retrieve the content if it hasn't changed
            if os.path.exists(port.download_filename()):
                existing_file_length = os.path.getsize(port.download_filename())
            else:
                existing_file_length = 0

            # Open URL.
            try:
                url_handle = urlopen(request)
            except HTTPError as http_err:
                if http_err.code == 304:
                    # resource not modified
                    # self.env["download_changed"] = False
                    logging.debug("Item at URL is unchanged.")
                    logging.debug("Using existing %s" % port.download_filename())
                    return
                else:
                    raise

            # If Content-Length header is present and we had a cached
            # file, see if it matches the size of the cached file.
            # Useful for webservers that don't provide Last-Modified
            # and ETag headers.
            size_header = url_handle.info().get("Content-Length")
            if url_handle.info().get("Content-Length"):
                if int(size_header) == existing_file_length:
                    # self.env["download_changed"] = False
                    logging.debug("Using existing %s" % port.download_filename())
                    return

            # Handle edge case where server responds with a
            # 'Content-Encoding: gzip' header, even though we've requested the
            # default 'Accept-Encoding: identity'
            content_encoding = url_handle.info().get('Content-Encoding', '').lower()
            if content_encoding == 'gzip':
                # notes on window bit size from http://www.zlib.net/manual.html
                # "windowBits can also be greater than 15 for optional gzip
                # decoding. Add 32 to windowBits to enable zlib and gzip
                # decoding with automatic header detection, or add 16 to decode
                # only the gzip format (the zlib format will return a
                # Z_DATA_ERROR)."
                #
                # Therefore, we explicitly set the window buffer size to
                # the width for decoding only gzip. zlib.MAX_WBITS is the 15
                # mentioned above.
                pass
            elif content_encoding and content_encoding != 'identity':
                logging.warning("WARNING:Content-Encoding of %s may not be "
                                "supported" % content_encoding)

            gzip_handle = zlib.decompressobj(16 + zlib.MAX_WBITS)

            # Download file.
            # self.env["download_changed"] = True
            logging.debug("Downloading {PORT}".format(PORT=port.name))
            with open(port.download_filename(), "wb") as file_handle:
                while True:
                    data = url_handle.read(CHUNK_SIZE)
                    if len(data) == 0:
                        break
                    if content_encoding == 'gzip':
                        data = gzip_handle.decompress(data)
                    file_handle.write(data)

            logging.debug("Downloaded %s" % port.download_filename())
            shutil.rmtree(port.sources_root(), ignore_errors=True)
            os.makedirs(port.sources_root())
            patoolib.extract_archive(port.download_filename(), outdir=port.sources_root())
        except BaseException as err:
            raise Exception("Couldn't download %s: %s" % (port.download_url(), err))

        finally:
            if url_handle is not None:
                url_handle.close()

    def download(self, port):
        if hasattr(port, 'source'):
            if 'hg' in port.source:
                logging.debug('Downloading using Mercurial')
                self.hg_get(port)
            elif 'git' in port.source:
                logging.debug('Downloading using git')
                self.git_get(port)
            elif 'svn' in port.source:
                logging.debug('Downloading using Subversion')
                self.svn_get(port)
            elif 'file' in port.source:
                logging.debug('Downloading using http-file')
                self.file_get(port)
            else:
                raise Exception('No Supported Source found in the Metadata')
        else:
            raise Exception('No Source attribute found in Metadata')
