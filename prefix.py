from config import ConfigurationManager


class Prefix:
    @staticmethod
    def change(newname):
        ConfigurationManager.save('prefix', '/opt/' + newname)

    @staticmethod
    def print():
        prefix = ConfigurationManager.get('prefix')
        if prefix is None:
            return '/opt/ports'
        else:
            return prefix
