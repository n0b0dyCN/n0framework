import requests
import Queue
import threading
import config
from time import sleep



class Flag:
    def __init__(self, flag, ip, port, payload):
        self.flag = str(flag)
        self.ip = ip
        self.port = port
        self.payload = payload

class Submitter(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self,name="Submitter")
        self.flagq = Queue.Queue()
        self.isrun = True

    def correct_flag(self, r):
        return True

    def stop(self):
        self.isrun = False

    def submit(self, flag):
        print "[submit] "
        url = "https://www.n0b0dycn.me"
        data = {
            "flag":flag.flag,
            "token":config.FLAG_TOKEN
        }
        r = requests.post(url, data=data)
        report(flag, self.correct_flag(r.text))

    def report(self, flag, correct):
        if correct:
            msg = "Attack {ip}:{port} with payload {payload} success.".format(ip=flag.ip, port=flag.port, payload=payload)
        else:
            msg = "Attack {ip}:{port} with payload {payload} failed.".format(ip=flag.ip, port=flag.port, payload=payload)

    def add(self, flag):
        print "Flag added."
        self.flagq.put(flag)

    def run(self):
        while self.isrun:
            try:
                if self.flagq.empty():
                    print "empty"
                    sleep(3)
                else:
                    print "Not empty"
                    flag = self.flagq.get()
                    print "[*] ", flag.flag
                    self.submit(flag)
            except Exception as e:
                msg = str(e)

