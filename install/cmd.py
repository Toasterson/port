from argcommand import Command


class InstallCommand(Command):
    """
    Install a Port
    """

    command_name = 'install'

    def run(self):
        print("installing")
