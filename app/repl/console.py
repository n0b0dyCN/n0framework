#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from prompt_toolkit import PromptSession, AbortAction, Application, CommandLineInterface
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer, Completion


class Console:
    def __init__(self):
        self.prompt = u"$ "
        self.banner = ""
        self.session = PromptSession(history=FileHistory('/tmp/history.txt'))    
        self.error_prompt = u"*** "
        self.info_prompt = u"[+] "
        self.commands = sorted([func[3:] for func in dir(self) if func[0:3]=="do_" and callable(getattr(self, func))])
        self.doced_commands = [func for func in self.commands if "help_"+func in dir(self) and callable(getattr(self, "help_"+func))]
        self.undoced_commands = list(set(self.commands).difference(set(self.doced_commands)))

    def do_test(self, arg):
        print("This is test function")
        print(repr(self))
        print(arg)


    def do_help(self, arg):
        if not arg:
            print("Help Manual")
            if self.doced_commands:
                print("Documented commands(type help <topic>):")
                print("="*25)
                for each in self.doced_commands:
                    print(each+"\t")
            if self.undoced_commands:
                if self.doced_commands:
                    print("")
                print("Undocumented commands:")
                print("="*25)
                for each in self.undoced_commands:
                    print(each+"\t")
            return
        else:
            commands = [i for i in arg.split(" ") if i]
            unfound = []
            undoced = []
            for c in commands:
                if c not in self.commands:
                    unfound.append(c)
                    continue
                if c not in self.doced_commands:
                    undoced.append(c)
                    continue
                print("Help for command '{c}':".format(c=c))
                getattr(self, "help_"+c)()
                print("")

    def help_help(self):
        print ("show help")

    def cmdloop(self):
        print(self.banner)
        while True:
            try:
                line = self.session.prompt(self.prompt)
                op = line.split(' ')[0]
                arg = line[len(op):].strip()
                try:
                    getattr(self, "do_"+op)(arg)
                except AttributeError as e:
                    self.error("Unknown command '{}'".format(op))
                except Exception as e:
                    self.error("Operation not supported.")
                    print(e)
            except KeyboardInterrupt:
                break
            except EOFError:
                break
        print("goodbye")

    def error(self, msg):
        print self.error_prompt, msg

    def info(self, msg):
        print self.info_prompt, msg


class Mycmd(Console):
    def __init__(self):
        Console.__init__(self)

    def do_testmy(self, arg):
        print("testmy")

    def help_testmy(self):
        print("help testmy")

def test():
    c = Mycmd()
    c.cmdloop()

test()
