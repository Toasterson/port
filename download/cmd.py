from argcommand import Command
from downloadmanager import DownLoadManager
from port import Port

class DownloadCommand(Command):
    """
    Download a Port
    """

    command_name = 'download'

    def run(self):
        port = Port()
        mgr = DownLoadManager()
        mgr.download(port)
        mgr.extract(port)
