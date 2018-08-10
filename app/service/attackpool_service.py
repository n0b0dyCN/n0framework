from __future__ import unicode_literals
import os
import imp
import shlex
import prettytable
import multiprocessing
import threading

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

from .service import Service
from core.nlog import NLog

class Attacker(Service, threading.Thread):
    def __init__(self):
        pass

    def name(self):
        return "attacker"

    def description(self):
        return "Attacker based on multiprocessing."

    def start(self, *args, **kwargs):
        self.log = NLog(self.name)
        self.log.info("Service attacker inited.")
        threading.Thread.start(self, *args, **kwargs)

    def stop(self):
        self.log.info("Service attacker stopped.")

    def setDaemon(self, *args, **kwargs):
        threading.Thread.setDaemon(self, *args, **kwargs)

    def make_parser(self, superparser):
        if not superparser:
            msg = "Need to give super parser"
            self.log.error(msg)
        subp = superparser.add_parser(self.name(), help=self.description())
        subp.add_argument("action", type=str, help="service action")

    def do(self, action):
        pass

    def run(self):
        atk_round = -1
        pass
