from ConfigParser import ConfigParser
from prettytable import PrettyTable


from .util import safeGetAttr

class Gamebox:
    def __init__(self, name, ip, port, in_ip, in_port,
                 ssh_port, ssh_user, ssh_pass):
        self.name     = name
        self.ip       = ip
        self.port     = int(port)
        self.in_ip    = in_ip
        self.in_port  = int(in_port)
        self.ssh_port = int(ssh_port)
        self.ssh_user = ssh_user
        self.ssh_pass = ssh_pass

    def getIP(self):
        return self.ip

    def getPort(self):
        return self.port

    def __str__(self):
        ret = "[gamebox] {name}".format(name=self.name)
        return ret


class GameboxManager:
    def __init__(self, confpath):
        self.cfg = ConfigParser()
        self.cfg.read(confpath)
        self.gameboxs = []

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
