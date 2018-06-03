import imp
import os
import sys
import re
import requests
import ConfigParser
import prettytable
import importlib

from . import config
from . import gamebox

def getExps():
    explist = []
    for f in os.listdir(config.EXP_PATH):
        if os.path.isfile(config.EXP_PATH + os.sep + f):
            if f[-3:] == ".py":
                explist.append(f[:-3])
    return explist

def loadExp(exp_name):
    """
    Load an exploit and return an exploit object.

    Args:
        exp_name: Script name of the exploit

    Returns:
        An exploit object.
    """
    #f, fpath, desc = imp.find_module(exp_name, config.EXP_PATH)
    try:
        mod = imp.load_source(exp_name,
                    "{base}{fn}.py".format(config.EXP_PATH, exp_name))
        obj = mod.Exploit()
        return obj 
    except Exception as e:
        msg = "Cannot load exploit `{exp_name}`".format(exp_name=exp_name)
        return None

def loadAllExps():
    exps = getExps()
    ret = []
    for exp in exps:
        print exp
        e = loadExp(exp)
        if e != None:
            ret.append(e)
    return ret

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

def getConfig(confpath):
    cfg = ConfigParser.ConfigParser()
    cfg.read(confpath)
    return cfg

def getGameboxs(cfg):
    secs = cfg.sections()
    gameboxs = []
    for sec in secs:
        gameboxs.append(
            gamebox.Gamebox(
                sec,
                cfg.get(sec, "IP"),
                cfg.get(sec, "PORT"),
                cfg.get(sec, "INNER_IP"),
                cfg.get(sec, "INNER_PORT"),
                cfg.get(sec, "SSH_PORT"),
                cfg.get(sec, "SSH_USER"),
                cfg.get(sec, "SSH_PASS")
            )
        )
    return gameboxs

def safeGetAttr(x, attr):
    if hasattr(x, attr):
        return getattr(x, attr)
    else:
        return None

def printGameboxs(gbs):
    x = lambda x,y: safeGetAttr(x,y)
    pt = prettytable.PrettyTable(['name', "ip", "port"])
    for gb in gbs:
        pt.add_row([
            x(gb, "name"),
            x(gb, "ip"),
            x(gb, "port")
        ])
    print(pt)

def printExps(exps):
    x = lambda x,y: safeGetAttr(x,y)
    pt = prettytable.PrettyTable(["file", "target", "author", "level", "timeout"])
    for exp in exps:
        pt.add_row([
            x(exp, "fname"),
            x(exp, "target"),
            x(exp, "author"),
            x(exp, "level"),
            x(exp, "timeout")
        ])
    print(pt)

def getExpNameByPath(s):
    bname = os.path.basename(s)
    if bname.endswith(".py"):
        return bname[:-3]
    if bname.endswith(".pyc"):
        return bname[:-4]

