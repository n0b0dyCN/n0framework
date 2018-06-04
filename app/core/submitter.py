import requests
import Queue
import threading
from time import sleep


class Flag:
    def __init__(self, flag, ip, port, payload):
        self.flag = str(flag)
        self.ip = ip
        self.port = port
        self.payload = payload

class Submitter(threading.Thread):
    def __init__(self, token=""):
        threading.Thread.__init__(self,name="Submitter")
        self.flagq = Queue.Queue()
        self.isrun = True
        self.token = token

    def correct_flag(self, r):
        return True

    def stop(self):
        self.isrun = False

    def submit(self, flag):
        url = "https://www.n0b0dycn.me"
        data = {
            "flag":flag.flag,
            "token":self.token
        }
        r = requests.post(url, data=data)
        report(flag, self.correct_flag(r.text))

    def report(self, flag, correct):
        if correct:
            msg = "Attack {ip}:{port} with payload {payload} success.".format(ip=flag.ip, port=flag.port, payload=payload)
        else:
            msg = "Attack {ip}:{port} with payload {payload} failed.".format(ip=flag.ip, port=flag.port, payload=payload)

    def add(self, flag, ip, port, payload):
        f = Flag(flag ,ip, port, payload)
        self.flagq.put(f)

    def run(self):
        while self.isrun:
            try:
                if self.flagq.empty():
                    sleep(3)
                else:
                    flag = self.flagq.get()
                    self.submit(flag)
            except Exception as e:
                msg = str(e)

