import imp
import os
import sys
import config
import re
import requests

def getExps():
    explist = []
    for f in os.listdir(config.EXP_PATH):
        if os.path.isfile(config.EXP_PATH + os.sep + f):
            if f[-3:] == ".py":
                explist.append(f[:-3])
    return explist

def importExp(exp_name):
    f, fpath, desc = imp.find_module(exp_name, config.EXP_PATH)
    try:
        mod = imp.load_module(exp_name, f, fpath, desc)
        return mod
    except ImportError as e:
        return None
    except Exception as e:
        return None

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

