import yaml
import io


class ConfigurationManager:
    @staticmethod
    def get(key):
        try:
            with io.open('~/.ports/config.yaml', 'r+') as config_desc:
                config = yaml.load(config_desc)
                if hasattr(config, key):
                    return config[key]
                else:
                    return None
        finally:
            return None

    @staticmethod
    def mget(keys):
        try:
            with io.open('~/.ports/config.yaml', 'r+') as config_desc:
                config = yaml.load(config_desc)
                retarr = {}
                for key in keys:
                    if hasattr(config, key):
                        retarr[key] = config[key]
                return retarr
        finally:
            return {}

    @staticmethod
    def save(key, value):
        with io.open('~/.ports/config.yaml', 'w+') as config_desc:
            config = yaml.load(config_desc)
            config.update(key, value)
            yaml.dump(config, config_desc)
