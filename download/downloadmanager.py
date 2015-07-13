import os
import urllib2
import zlib
import patoolib
import shutil

# Download URLs in chunks of 256 kB.
CHUNK_SIZE = 256 * 1024

# # XATTR names for Etag and Last-Modified headers
# XATTR_ETAG = "illumos-ports.etag"
# XATTR_LAST_MODIFIED = "illumos-ports.last-modified"
#
#
# def getxattr(pathname, attr):
#     """Get a named xattr from a file. Return None if not present"""
#     if attr in xattr.listxattr(pathname):
#         return xattr.getxattr(pathname, attr)
#     else:
#         return None

class DownLoadManager(object):
    def __init__(self):
        pass

    def download(self, port):
        # create download cache if needed
        if not os.path.exists(port.download_dir()):
            os.makedirs(port.download_dir())

        # Download URL.
        url_handle = None
        try:
            request = urllib2.Request(url=port.download_url())

            # if file already exists, add some headers to the request
            # so we don't retrieve the content if it hasn't changed
            if os.path.exists(port.download_filename()):
                # etag = getxattr(port_download_file, XATTR_ETAG)
                # last_modified = getxattr(port_download_file, XATTR_LAST_MODIFIED)
                # if etag:
                #    request.add_header("If-None-Match", etag)
                # if last_modified:
                #    request.add_header("If-Modified-Since", last_modified)
                existing_file_length = os.path.getsize(port.download_filename())
            else:
                existing_file_length = 0

            # Open URL.
            try:
                url_handle = urllib2.urlopen(request)
            except urllib2.HTTPError, http_err:
                if http_err.code == 304:
                    # resource not modified
                    # self.env["download_changed"] = False
                    # self.output("Item at URL is unchanged.")
                    # self.output("Using existing %s" % port_download_file)
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
                    # self.output("File size returned by webserver matches that "
                    #             "of the cached file: %s bytes" % size_header)
                    # self.output("WARNING: Matching a download by filesize is a "
                    #             "fallback mechanism that does not guarantee "
                    #             "that a build is unchanged.")
                    # self.output("Using existing %s" % port_download_file)
                    print("{PORT} already downloaded skipping").format(PORT=port.name)
                    return

            # Handle edge case where server responds with a
            # 'Content-Encoding: gzip' header, even though we've requested the
            # default 'Accept-Encoding: identity'
            content_encoding = url_handle.info().get('Content-Encoding', '').lower()
            # if content_encoding == 'gzip':
            #     # notes on window bit size from http://www.zlib.net/manual.html
            #     # "windowBits can also be greater than 15 for optional gzip
            #     # decoding. Add 32 to windowBits to enable zlib and gzip
            #     # decoding with automatic header detection, or add 16 to decode
            #     # only the gzip format (the zlib format will return a
            #     # Z_DATA_ERROR)."
            #     #
            #     # Therefore, we explicitly set the window buffer size to
            #     # the width for decoding only gzip. zlib.MAX_WBITS is the 15
            #     # mentioned above.
            #
            # elif content_encoding and content_encoding != 'identity':
            #     # self.output("WARNING: Content-Encoding of %s may not be "
            #     #             "supported" % content_encoding)
            #
            gzip_handle = zlib.decompressobj(16 + zlib.MAX_WBITS)

            # Download file.
            # self.env["download_changed"] = True
            print("Downloading {PORT}").format(PORT=port.name)
            with open(port.download_filename(), "wb") as file_handle:
                while True:
                    data = url_handle.read(CHUNK_SIZE)
                    if len(data) == 0:
                        break
                    if content_encoding == 'gzip':
                        data = gzip_handle.decompress(data)
                    file_handle.write(data)

                    # # save last-modified header if it exists
                    # if url_handle.info().get("last-modified"):
                    #     self.env["last_modified"] = (
                    #         url_handle.info().get("last-modified"))
                    #     xattr.setxattr(
                    #         port_download_file, XATTR_LAST_MODIFIED,
                    #         url_handle.info().get("last-modified"))
                    #     self.output(
                    #         "Storing new Last-Modified header: %s"
                    #         % url_handle.info().get("last-modified"))
                    #
                    # # save etag if it exists
                    # self.env["etag"] = ""
                    # if url_handle.info().get("etag"):
                    #     self.env["etag"] = url_handle.info().get("etag")
                    #     xattr.setxattr(
                    #         port_download_file, XATTR_ETAG, url_handle.info().get("etag"))
                    #     self.output("Storing new ETag header: %s"
                    #                 % url_handle.info().get("etag"))
                    #
                    # self.output("Downloaded %s" % port_download_file)
                    # self.env['url_downloader_summary_result'] = {
                    #     'summary_text': 'The following new items were downloaded:',
                    #     'data': {
                    #         'download_path': port_download_file,
                    #     }
                    # }

                    # except BaseException as err:
                    # raise ProcessorError(
                    #     "Couldn't download %s: %s" % (self.env["url"], err))
        finally:
            if url_handle is not None:
                url_handle.close()

    def extract(self, port):
        shutil.rmtree(port.source_dir(), ignore_errors=True)
        os.makedirs(port.source_dir())
        patoolib.extract_archive(port.download_filename(), outdir=port.source_dir())
