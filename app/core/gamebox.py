from ConfigParser import ConfigParser
from prettytable import PrettyTable


from .util import safeGetAttr, getLog

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

