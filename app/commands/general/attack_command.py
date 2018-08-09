from __future__ import unicode_literals
import sys
import shlex

from prompt_toolkit.completion import WordCompleter

from ..command import Command
from ..command_arg_parser import CommandArgParser
from core.util import genIPList, parseline


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
        print "Do attack"
        reg = kwargs["serviceReg"]
        gameboxs = reg.get("gamebox").getGameboxs()
        for gb in gameboxs:
            exps = reg.get("exploit").getExpByTarget(gb.name)
            ips = genIPList(gb.getIP())
            port = gb.getPort()
            for ip in ips:
                for e in exps:
                    self.attack_target(ip, port, e, reg)

    def attack_target(self, ip, port, exp, reg):
        flag = exp.attack(ip, port)
        reg.get("submitter").add(flag, ip, port, exp.name)

    def make_parser(self, **kwargs):
        parser = CommandArgParser()
        parser.add_argument("--team", action="store", dest="team")
        parser.add_argument("--exp", action="store", dest="exp")
        parser.add_argument("--ip", action="store", dest="ip")
        parser.add_argument("--gamebox", action="store", dest="gamebox")
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

