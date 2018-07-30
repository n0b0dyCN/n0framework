import json

class Flag:
    def __init__(self, flag, ip, port, payload):
        self.flag = str(flag)
        self.ip = ip
        self.port = port
        self.payload = payload

    def __str__(self):
        d = {
            "flag": self.flag,
            "ip": self.ip,
            "port": self.port,
            "payload": self.payload
        }
        return json.dumps(d)
