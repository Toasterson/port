from config import ConfigurationManager


class Prefix:
    @staticmethod
    def change(newname):
        ConfigurationManager.save('prefix', '/opt/' + newname)

    @staticmethod
    def print():
        return ConfigurationManager.get('prefix', '/opt/ports')
