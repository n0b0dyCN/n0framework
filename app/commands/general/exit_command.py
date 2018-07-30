from __future__ import unicode_literals
import sys

from ..command import Command


class ExitCommand(Command):
    def __init__(self):
        pass

    def name(self):
        return "exit"

    def description(self):
        return "Exit the framework"

    def action(self, args=None, **kwargs):
        if "serviceReg" in kwargs:
            kwargs["serverReg"].stopall()
        sys.exit(0)

    def make_parser(self, **kwargs):
        return None

    def make_completer(self):
        return None
