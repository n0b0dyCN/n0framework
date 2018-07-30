
from __future__ import unicode_literals

class CommandRegister:
    def __init__(self):
        self.__commands = {} # name => instance
    
    def register(self, command):
        if command.name() in self.__commands:
            raise ValueError("Command already registered: {}".format(command.name()))
        self.__commands[command.name()] = command

    def erase(self, name):
        if name not in self.__commands:
            raise ValueError("Command not registered: {}".format(name))
        self.__commands.pop(name)

    def get(self, name):
        if name in self.__commands:
            return self.__commands[name]
        return None

    @property
    def count(self):
        return len(self.__commands)

    def commands(self):
        return self.__commands.values()

    def names(self):
        return self.__commands.keys()

    def getCompleter(self, name, **kwargs):
        ins = self.get(name.strip().lower())
        if not ins:
            return None
        c = ins.make_completer(**kwargs)
        return c

    def action(self, name, args=None, **kwargs):
        cmd = self.get(name)
        if cmd:
            cmd.action(args, **kwargs)
        else:
            msg = "Command {} not found".format(name)
