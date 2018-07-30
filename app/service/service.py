# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from abc import ABCMeta, abstractmethod
import re

from prompt_toolkit.completion import WordCompleter

class Service(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def name(self):
        return "service"

    @abstractmethod
    def description(self):
        return "description"

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def start(self, *args, **kwargs):
        pass

    @abstractmethod
    def setDaemon(self, *args, **kwargs):
        pass

    @abstractmethod
    def make_parser(self, superparser):
        pass

    @abstractmethod
    def do(self, action):
        pass

    @staticmethod
    def find_all():
        services = set()
        for child in Service.__subclasses__():
            if child not in services:
                services.add(child)
        return list(services)

