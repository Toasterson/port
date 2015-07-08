from argcommand import Command


class DownloadCommand(Command):
    """
    Download a Port
    """

    command_name = 'download'

    def run(self):
        print("downloading")
