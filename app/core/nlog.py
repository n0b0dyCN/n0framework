import logging

class NLog:
    def __init__(self, log_name):
        self.log = logging.getLogger(log_name)
        self.log.setLevel(logging.DEBUG)

        handler = logging.FileHandler("/framelog/{name}.log".format(name=log_name))
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(message)s",
                                     datefmt="%m/%d/%Y %H:%M:%S %p")
        handler.setFormatter(formatter)
        self.log.addHandler(handler)

    def info(self, msg):
        self.log.info(msg)

    def error(self, msg):
        self.log.error(msg)

    def debug(self, msg):
        self.log.debug(msg)

    def warn(self, msg):
        self.log.warn(msg)

    def critical(self, msg):
        self.log.critical(msg)
