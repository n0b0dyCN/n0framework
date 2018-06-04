#!/usr/local/bin/python
#-*- coding:utf-8 -*-

import signal
import cmd
from prettytable import PrettyTable
from ConfigParser import ConfigParser

from core import util
from core.submitter import Submitter
from core.expmanager import ExpManager
from core.gamebox import GameboxManager


class FrameworkShell(cmd.Cmd):
    def __init__(self, general_conf):
        cmd.Cmd.__init__(self)
        self.prompt = "➜ "
        
        self.general_cfg = ConfigParser()
        self.general_cfg.read(general_conf)


        self.flag_submitter = Submitter(
            self.general_cfg.get("GENERAL", "FLAG_TOKEN")
        )
        self.flag_submitter.setDaemon(True)
        self.flag_submitter.start()

        self.exp_manager = ExpManager(
            self.general_cfg.get("GENERAL", "EXP_PATH")
        )
        self.gamebox_manager = GameboxManager(
            self.general_cfg.get("GENERAL", "GAMEBOX_CONFIG")
        )

    
    def preloop(self):
        banner = """
        N0Framework
        Powered by n0b0dy@Eur3kA
        """
        print banner

    def postloop(self):
        pass

    def do_exit(self, arg):
        self.flag_submitter.stop()
        return True

    def help_exit(self):
        print "Exit."

    def do_loadGameboxs(self, arg):
        self.gamebox_manager.loadGameboxs()

    def help_loadGameboxs(self):
        print "Load gamebox information."

    def do_showGameboxs(self, arg):
        self.gamebox_manager.printGameboxs()

    def help_showGameboxs(self):
        print "Show gameboxs information."

    def do_loadExps(self, arg):
        self.exp_manager.loadAllExps()

    def help_loadExps(self):
        print "Load all exploits."

    def do_showExps(self, arg):
        self.exp_manager.printExps()

    def help_showExps(self):
        print "Show exploits information."

    def do_reloadExp(self, arg):
        if arg == '':
            # if no exp specified, reload all exps.
            self.exp_manager.reload()
        else:
            self.exp_manager.reload([i for i in arg.split() if i != ""])
 
    def help_reloadExp(self):
        print "Reload specific exps (seperated with space) if arg given, or reload all."
        print "Examples:"
        print "To reload exp1 and exp2: `reloadExp exp1 exp2`"
        print "To reload all exps: `reload`"

    def do_attack(self, arg):
        gbs = self.gamebox_manager.getGameboxs()
        for gb in gbs:
            exps = self.exp_manager.getExpByTarget(gb.name)
            ips = util.genIPList(gb.getIP())
            port = gb.getPort()
            for e in exps:
                for ip in ips:
                    flag = e.attack(ip, port)
                    self.flag_submitter.add(flag, ip, port, e.fname)

    def help_attack(self):
        print "Attack using all exploits"

if __name__ == "__main__":
    cmd = FrameworkShell("/app/config/general.cfg")
    cmd.cmdloop()
