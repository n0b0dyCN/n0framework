# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from abc import ABCMeta, abstractmethod
import re

from prompt_toolkit.completion import WordCompleter

from .command_arg_parser import ParserExitException

class Command(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def name(self):
        return "name"

    @abstractmethod
    def description(self):
        return "description"

    @abstractmethod
    def action(self, args=None, **kwargs):
        pass

    @abstractmethod
    def make_parser(self, **kwargs):
        pass

    @abstractmethod
    def make_completer(self):
        pass

    def parse_args(self, args, **kwargs):
        parser = self.make_parser(**kwargs)
        ret = None
        if not parser:
            return None
        try:
            ret = parser.parse_args(args)
        except ParserExitException as e:
            pass
        except Exception as e:
            pass
        return ret

    @staticmethod
    def find_all():
        cmds = set()
        for child in Command.__subclasses__():
            if child not in cmds:
                cmds.add(child)
        return list(cmds)

