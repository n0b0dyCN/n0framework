import os
import sys
import re
import requests
import logging
import shlex


def genIPList(ips):
    try:
        ip_pattern = "^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])(.\d{1,2}|1\d\d|2[0-4]\d|25[0-5]){3}$"
        ip_re = re.compile(ip_pattern)
        if "-" not in ips:
            if ip_re.match(ips) != None:
                return [ips]
            else:
                return []

        parts = ips.split(".")
        if len(parts) != 4:
            return []
        pl = []
        for part in parts:
            if "-" in part:
                s, e = part.split("-")
                s = int(s)
                e = int(e)
                pl.append(range(s, e+1))
            else:
                pl.append([int(part)])

        ret = []
        for A in pl[0]:
            for B in pl[1]:
                for C in pl[2]:
                    for D in pl[3]:
                        ret.append(
                            "{A}.{B}.{C}.{D}".format(A=A,B=B,C=C,D=D)
                        )

        return ret
    except Exception as e:
        return []


def safeGetAttr(x, attr):
    if hasattr(x, attr):
        return getattr(x, attr)
    else:
        return None


def getLog(name):
    log = logging.getLogger("n0framework.{name}".format(name=name))
    log.setLevel(logging.DEBUG)

    handler = logging.FileHandler("/framelog/{name}.log".format(name=name))
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(message)s",
                                 datefmt="%m/%d/%Y %H:%M:%S %p")
    handler.setFormatter(formatter)
    log.addHandler(handler)
    return log

def parseline(line):
    if isinstance(line, list):
        return (line[0], line[1:])
    try:
        if ' ' in line:
            cmd, args = line.split(' ', 1)
            return (cmd, shlex.split(args))
    except ValueError:
        pass
    return (line.strip(), None)

