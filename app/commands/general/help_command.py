from __future__ import unicode_literals
import argparse

from prompt_toolkit.completion import WordCompleter

from ..command import Command
from ..command_arg_parser import CommandArgParser

class HelpCommand(Command):
    def __init__(self):
        pass

    def name(self):
        return "help"

    def description(self):
        return "Show help"

    def action(self, args=None, **kwargs):
        if "commandReg" not in kwargs:
            msg = "Need commandReg in action parameters"
            print msg
        reg = kwargs["commandReg"]
        if args:
            ins = reg.get(args.cmd)
            if not ins:
                print("\tCommand not found: {}".format(c))
                return
            self.showCmd(ins)
            return
        for i in reg.commands():
            self.showCmd(i)

    def make_completer(self, **kwargs):
        if "commandReg" in kwargs:
            return WordCompleter(kwargs["commandReg"].names())
        return None

    def make_parser(self, **kwargs):
        parser = CommandArgParser()
        parser.add_argument("cmd", action="store", type=str)
        return parser

    def showCmd(self, cmd):
        msg = "\t{name}\n"
        msg += "\t\t{desc}"
        print msg.format(name=cmd.name(), desc=cmd.description())

