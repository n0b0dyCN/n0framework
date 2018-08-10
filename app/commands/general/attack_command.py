from __future__ import unicode_literals
import sys
import shlex
import copy
import threading
import time

from prompt_toolkit.completion import WordCompleter

from ..command import Command
from ..command_arg_parser import CommandArgParser
from core.util import genIPList, parseline

class AttackThread(threading.Thread):
    def __init__(self, reg):
        threading.Thread.__init__(self)
        self.isrun = True
        self.reg = reg

    def stop(self):
        self.isrun = False

    def run(self):
        while self.isrun:
            gameboxs = self.reg.get("gamebox").getGameboxs()
            for gb in gameboxs:
                exps = self.reg.get("exploit").getExpByTarget(gb.name)
                ips = genIPList(gb.getIP())
                port = gb.getPort()
                for ip in ips:
                    for e in exps:
                        self.attack_target(ip, port, e, self.reg)
            time.sleep(10)

    def attack_target(self, ip, port, exp, reg):
        ee = exp.Exploit()
        ee.set(ip=ip, port=port, submitter=reg.get("submitter"))
        ee.setDaemon(True)
        ee.start()



class AttackWordCompleter(WordCompleter):
    def __init__(self,  actions=None,
                 ips=None, team_names=None, exp_names=None, gamebox_names=None):
        self.actions = actions
        self.ips = ips
        self.team_names = team_names
        self.exp_names = exp_names
        self.gamebox_names = gamebox_names
        super(AttackWordCompleter, self).__init__(self.actions)

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor.lstrip()
        if ' ' in text:
            cmd, args = parseline(text)
            if len(args) > 0:
                opt = args[-1]
                if opt == "--team":
                    return WordCompleter(self.team_names).get_completions(document, complete_event)
                elif opt == "--ip":
                    return WordCompleter(self.ips).get_completions(document, complete_event)
                elif opt == "--gamebox":
                    return WordCompleter(self.gamebox_names).get_completions(document, complete_event)
                elif opt == "--exp":
                    return WordCompleter(self.exp_names).get_completions(document, complete_event)
        return super(AttackWordCompleter, self).get_completions(document, complete_event)

class AttackCommand(Command):
    def __init__(self):
        self.attack_thread = None
        pass

    def name(self):
        return "attack"

    def description(self):
        return "Using exploits to attack targets"

    def action(self, args=None, **kwargs):
        if "serviceReg" not in kwargs:
            msg = "Service register needed."
            print msg
            return
        reg = kwargs["serviceReg"]
        if args == None or args.action == "restart":
            if args != None:
                self.attack_thread.stop()
            self.attack_thread = AttackThread(reg)
            self.attack_thread.setDaemon(True)
            self.attack_thread.start()
        elif args.action == "stop":
            self.attack_thread.stop()
        elif args.action == "start":
            if self.attack_thread and self.attack_thread.isrun:
                print "Attack already started."
            else:
                self.attack_thread = AttackThread(reg)
                self.attack_thread.setDaemon(True)
                self.attack_thread.start()
        else:
            msg = "Unknown command {}".format(args.action)
            print msg
        return
        gameboxs = reg.get("gamebox").getGameboxs()
        for gb in gameboxs:
            exps = reg.get("exploit").getExpByTarget(gb.name)
            ips = genIPList(gb.getIP())
            port = gb.getPort()
            for ip in ips:
                for e in exps:
                    self.attack_target(ip, port, e, reg)

    def attack_target(self, ip, port, exp, reg):
        ee = exp.Exploit()
        ee.set(ip=ip, port=port, submitter=reg.get("submitter"))
        ee.start()

    def make_parser(self, **kwargs):
        parser = CommandArgParser()
        parser.add_argument("action", type=str, help="service action")
        return parser

    def get_actions(self):
        return ["--team", "--exp", "--ip", "--gamebox"]

    def make_completer(self, **kwargs):
        if "serviceReg" not in kwargs:
            return None
        actions = self.get_actions()
        ips=kwargs["serviceReg"].get("gamebox").get_gamebox_ips()
        gamebox_names=kwargs["serviceReg"].get("gamebox").get_gamebox_names()
        exp_names=kwargs["serviceReg"].get("exploit").get_exp_names()
        c = AttackWordCompleter(
            actions = actions,
            ips=ips,
            gamebox_names=gamebox_names,
            exp_names=exp_names
        )
        return c

