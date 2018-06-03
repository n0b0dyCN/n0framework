
class Gamebox:
    def __init__(self, name, ip, port, in_ip, in_port,
                 ssh_port, ssh_user, ssh_pass):
        self.name     = name
        self.ip       = ip
        self.port     = port
        self.in_ip    = in_ip
        self.in_port  = in_port
        self.ssh_port = ssh_port
        self.ssh_user = ssh_user
        self.ssh_pass = ssh_pass


