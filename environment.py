import os
import re


def unbracket(string):
    if "{" in string:
        return string[1:-1]
    else:
        return string


class EnvironmentManager(object):
    def __init__(self):
        self.env = os.environ.copy()
        self.env["LD_LIBRARY_PATH"] = ''
        self.register = {}
        self.options = {}

    def getVariable(self, key):
        return self.env[unbracket(key)]

    def getEnvironment(self):
        return self.env

    def getOptions(self):
        return self.options

    def loadEnvironment(self, tup):
        if tup.get('environment') is not None:
            self.env.update(tup.get('environment'))

            for key, value in tup.get('environment').items():
                self.updateVariable(key, value)

    def updateVariable(self, key, value):
        if "{" in value:
            pat = re.compile("\{[^]]*\}")
            match = pat.search(value)
            reg_key = unbracket(match.group(0))
            reg_value = {key: value}
            value = value.replace('{' + reg_key + '}', self.env[reg_key])
            if reg_key in self.register.keys():
                if key not in self.register[reg_key]:
                    self.register[reg_key].update(reg_value)
            else:
                self.register[reg_key] = reg_value

        self.env[key] = value
        self.options[key] = value

        if key in self.register.keys():
            for key, value in self.register.get(key).items():
                self.updateVariable(key, value)
