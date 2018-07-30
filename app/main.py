#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import unicode_literals

from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory, InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.key_binding import KeyBindings

import shlex

from commands.command import Command
from commands.command_register import CommandRegister
from service.service import Service
from service.service_register import ServiceRegister

from core import util
from core.completer import Completer


class InteractiveShell:
    def __init__(self):
        self.prompt = "➜ "
        self.banner = """
        n0framework
        Powered by n0b0dy@Eur3kA
        """
        self.session = None 
        self.commandReg = CommandRegister()
        self.serviceReg = ServiceRegister()
        self.history = FileHistory("/framelog/history.txt")
        for cmd in Command.find_all():
            self.commandReg.register(cmd())
        for service in Service.find_all():
            self.serviceReg.register(service())


    def buildCompleter(self):
        cmds = self.commandReg.commands()
        words = []
        meta = {}
        for ins in cmds:
            words.append(ins.name())
            meta[ins.name()] = ins.description()
        return Completer(words=words, meta_dict=meta,
                         commandReg=self.commandReg,
                         serviceReg=self.serviceReg
                        )


    def process(self, line):
        if line == None:
            return True
        cmd, args = util.parseline(line.strip())
        ins = self.commandReg.get(cmd)
        if not ins:
            if cmd == '':
                return
            msg = "Command not found: '{}'".format(cmd)
            print msg
            return
        parsed_args = ins.parse_args(args,
                                     commandReg=self.commandReg,
                                     serviceReg=self.serviceReg
                                    )
        ins.action(parsed_args,
                   commandReg=self.commandReg,
                   serviceReg=self.serviceReg
                  )
        return False

    def get_kb(self):
        kb = KeyBindings()
        @kb.add('c-c')
        def _(event):
            l = len(event.app.current_buffer.document.text)
            event.app.current_buffer.delete_before_cursor(l)

        @kb.add('c-q')
        def _(event):
            event.app.exit()

        return kb

    def loop(self):
        self.completer = self.buildCompleter() 
        
        self.session = PromptSession(
            message=self.prompt,
            history=self.history,
            auto_suggest=AutoSuggestFromHistory(),
            completer=self.completer,
            key_bindings=self.get_kb()
        )

        print self.banner
        while True:
            line = self.session.prompt()
            stop = self.process(line)
            if stop:
                break

def main():
    i = InteractiveShell()
    i.loop()

main()
