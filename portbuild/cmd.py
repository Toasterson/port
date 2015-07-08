from argcommand import Command


class BuildCommand(Command):
    """
    Build a Port
    """

    command_name = 'build'

    def run(self):
        print("building")
