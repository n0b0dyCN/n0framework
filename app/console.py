#-*- coding:utf-8 -*-

import signal
import cmd
from prettytable import PrettyTable

from core import util, submitter

class ExpManager(cmd.Cmd):
    def __init__(self, conf):
        cmd.Cmd.__init__(self)
        self.prompt = "➜ "

        self.cfg = util.getConfig(conf)

        self.flag_submitter = submitter.Submitter()
        self.flag_submitter.setDaemon(True)
        self.flag_submitter.start()

        self.gameboxs = []
        self.exps = []

    
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
        self.gameboxs = util.getGameboxs(self.cfg)

    def help_loadGameboxs(self):
        print "Load gamebox information."

    def do_showGameboxs(self, arg):
        util.printGameboxs(self.gameboxs)

    def help_showGameboxs(self):
        print "Show gameboxs information."

    def do_loadExps(self, arg):
        self.exps = util.loadAllExps()

    def help_loadExps(self):
        print "Load all exploits."

    def do_showExps(self, arg):
        util.printExps(self.exps)

    def help_showExps(self):
        print "Show exploits information."

    def do_reloadExp(self, arg):
        if arg == '':
            # if no exp specified, reload all exps.
            self.exps[:] = []
            self.do_loadExps(arg)
        else:
            reload_exps = [e for e in arg.split(" ") if e != ""]
            if len(reload_exps) > 0:
                for exp_name in reload_exps:
                    for e in self.exps:
                        if util.getExpNameByPath(e.fname) == exp_name:
                            self.exps.remove(e)
                            break
                    obj = util.loadExp(exp)
                    if obj:
                        self.exps.append(exp)
 
    def help_reloadExp(self):
        print "Reload specific exps (seperated with space) if arg given, or reload all."
        print "Examples:"
        print "To reload exp1 and exp2: `reloadExp exp1 exp2`"
        print "To reload all exps: `reload`"



if __name__ == "__main__":
    cmd = ExpManager("/app/game.cfg")
    cmd.cmdloop()
