from __future__ import unicode_literals

from ..command import Command

class TestCommand(Command):
    def name(self):
        return "test"

    def description(self):
        return "A test command"

    def action(self, args=None, **kwargs):
        print("This is a test command.")
        print("args:")
        print(repr(args))

    def make_parser(self, **kwargs):
        return None

    def make_completer(self, **kwargs):
        return None
