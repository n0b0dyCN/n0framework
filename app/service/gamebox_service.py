from __future__ import unicode_literals

from ConfigParser import ConfigParser
from prettytable import PrettyTable
from core.util import safeGetAttr, getLog, genIPList

from .service import Service
from core.gamebox import Gamebox
from core.nlog import NLog

class GameboxService(Service):
    def __init__(self): 
        self.cfg = ConfigParser()
        confpath="/app/config/gamebox.cfg"
        self.cfg.read(confpath)
        self.gameboxs = []

    def name(self):
        return "gamebox"

    def description(self):
        return "Gamebox service store gamebox information."

    def stop(self):
        self.log.info("Service Gamebox stopped.")
        pass

    def start(self, *args, **kwargs):
        self.log = NLog(self.name())
        self.loadGameboxs()
        msg = ("Service Gamebox inited.")
        self.log.info(msg)

    def setDaemon(self, *args, **kwargs):
        pass

    def make_parser(self, superparser):
        if not superparser:
            msg = "Need to give super parser"
            self.log.error(msg)
        subp = superparser.add_parser(self.name(), help=self.description())
        subp.add_argument("action", type=str, help="service action")

    def do(self, action):
        if action == "show":
            self.printGameboxs()
        elif action == "load" or action == "reload":
            self.loadGameboxs()
        else:
            msg = "Unrecognized action for service {}: {}".format(self.name(), action)
            self.log.error(msg)
            print msg

    def loadGameboxs(self):
        secs = self.cfg.sections()
        self.gameboxs = []
        for sec in secs:
            self.gameboxs.append(
                Gamebox(
                    sec,
                    self.cfg.get(sec, "IP"),
                    self.cfg.get(sec, "PORT"),
                    self.cfg.get(sec, "INNER_IP"),
                    self.cfg.get(sec, "INNER_PORT"),
                    self.cfg.get(sec, "SSH_PORT"),
                    self.cfg.get(sec, "SSH_USER"),
                    self.cfg.get(sec, "SSH_PASS")
                )
            )

    def printGameboxs(self):
        x = lambda x,y: safeGetAttr(x,y)
        pt = PrettyTable(['name', "ip", "port"])
        for gb in self.gameboxs:
            pt.add_row([
                x(gb, "name"),
                x(gb, "ip"),
                x(gb, "port")
            ])
        print(pt)

    def getGameboxs(self):
        return self.gameboxs

    def getGameboxByName(self, name):
        for gb in self.gameboxs:
            if gb.name == name:
                return gb
        return None

    def get_gamebox_names(self):
        return [each.name for each in self.gameboxs]

    def get_gamebox_ips(self):
        ret = []
        for each in self.gameboxs:
            ret.extend(genIPList(each.ip))
        return ret

