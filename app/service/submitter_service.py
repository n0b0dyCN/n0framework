from __future__ import unicode_literals

import requests
import Queue
import threading
from time import sleep
import logging
from ConfigParser import ConfigParser

from .service import Service
from core.flag import Flag
from core.nlog import NLog

class SubmitterService(Service, threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self,name="Submitter")
        gc = ConfigParser()
        gc.read("/app/config/general.cfg")
        self.token = gc.get("GENERAL", "FLAG_TOKEN")

        self.flagq = Queue.Queue()
        self.isrun = True
        #self.token = token
        self.log = None

    def name(self):
        return "submitter"

    def description(self):
        return "Service used to submit flag and generate log."

    def stop(self):
        self.isrun = False
        self.log.info("Service submitter stopped.")

    def start(self, *args, **kwargs):
        self.log = NLog(self.name())
        self.log.info("Service submitter inited.")
        threading.Thread.start(self, *args, **kwargs)

    def make_completer(self):
        return None

    def make_parser(self, superparser=None):
        if not superparser:
            msg = "Need to give super parser"
        subp = superparser.add_parser(self.name(), help=self.description())
        subp.add_argument("action", type=str, help="service action")

    def setDaemon(self, *args, **kwargs):
        threading.Thread.setDaemon(self, *args, **kwargs)

    def do(self, action):
        if action == "help":
            print self.description()
        else:
            msg = "Unrecognized action for service {}: {}".format(self.name(), action)
            self.log.error(msg)

    def run(self):
        self.log.info("Submitter start running.")
        while self.isrun:
            try:
                if not self.flagq.empty():
                    flag = self.flagq.get()
                    self.submit(flag)
            except Exception as e:
                msg = str(e)
                self.log.error(e)
                #print(msg)

    def correct_flag(self, r):
        return {"status":"correct"}

    def submit(self, flag):
        url = "http://127.0.0.1:8099/"
        data = {
            "flag":flag.flag,
            "token":self.token
        }
        r = requests.post(url, data=data)
        self.report(flag, self.correct_flag(r.text))

    def report(self, flag, resp):
        msg = "Attack {ip}:{port} with payload {payload} {status}.".format(
            ip=flag.ip, port=flag.port, payload=flag.payload, status=resp["status"])
        print(msg)
        self.log.info("Report: " + msg)


    def add(self, flag, ip, port, payload):
        f = Flag(flag ,ip, port, payload)
        self.flagq.put(f)

