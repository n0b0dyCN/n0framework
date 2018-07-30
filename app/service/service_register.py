import argparse

from .service import Service

class ServiceRegister:
    def __init__(self):
        self.__services = {}
    
    def register(self, service):
        if isinstance(service, Service):
            self.__services[service.name()] = service

    def erase(self, name):
        if name in self.__services:
            self.__services.pop(name)

    def get(self, name):
        if name in self.__services:
            return self.__services[name]
        return None

    def count(self):
        return len(self.__services)

    def names(self):
        return self.__services.keys()

    def services(self):
        return self.__services.values()

    def start(self, serv_name):
        if serv_name in self.__services:
            self.__services[serv_name].setDaemon(True)
            self.__services[serv_name].start()
        else:
            msg = "Service not found: {}".format(serv_name)
            print msg

    def start_all(self):
        for k in self.__services:
            self.start(k)

    def stop(self, serv_name):
        if serv_name in self.__services:
            self.__services[serv_name].stop()
        else:
            msg = "Service not found: {}".format(serv_name)
            print msg

    def stop_all(self):
        for k in self.__services:
            self.stop(k)

    def handleReq(self, serv, action):
        if serv not in self.__services:
            msg = "Service not found: {}".format(serv)

        if serv == "all":
            if action == "start":
                self.start_all()
            elif action == "stop":
                self.stop_all()
            else:
                msg = "Unknown action: {}".format(action)
            return

        if action == "start":
            self.start(serv)
        elif action == "stop":
            self.stop(serv)

        return self.__services[serv].do(action)


