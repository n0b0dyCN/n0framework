import prettytable
import os
import imp

from .util import safeGetAttr, getLog

class ExpManager:
    def __init__(self, exppath):
        self.exppath = exppath
        self.exps = {}
        self.logger = getLog("expmanager")

    def getExps(self):
        explist = []
        for f in os.listdir(self.exppath):
            if os.path.isfile(self.exppath + os.sep + f):
                if f[-3:] == ".py":
                    explist.append(f[:-3])
        self.logger.info("{n} exploits found".format(n=len(explist)))
        return explist

    def loadExp(self, exp_name):
        """
        Load an exploit and return an exploit object.

        Args:
            exp_name: Script name of the exploit

        Returns:
            An exploit object if success, otherwise None.
        """
        try:
            exp_path = "{base}{fn}.py".format(base=self.exppath, fn=exp_name)
            mod = imp.load_source(exp_name, exp_path)
            obj = mod.Exploit()
            self.logger.info("Exploit `{exp_name}` loaded.".format(exp_name=exp_name))
            return obj 
        except Exception as e:
            msg = "Cannot load exploit `{exp_name}`".format(exp_name=exp_name)
            self.logger,error(msg)
            return None

    def loadAllExps(self):
        self.exps = []
        exists_exps = self.getExps()
        self.logger.info("Loading all exploits");
        ret = {}
        for exp in exists_exps:
            e = self.loadExp(exp)
            if e.target in ret:
                ret[e.target].append(e)
            else:
                ret[e.target] = [e]
        self.exps = ret

    def printExps(self):
        x = lambda x,y: safeGetAttr(x,y)
        exp_list = []
        for k in self.exps:
            exp_list.extend(self.exps[k])
        pt = prettytable.PrettyTable(["file", "target", "author", "level", "timeout"])
        for exp in exp_list:
            pt.add_row([
                x(exp, "fname"),
                x(exp, "target"),
                x(exp, "author"),
                x(exp, "level"),
                x(exp, "timeout")
            ])
        print(pt)

    def getExpNameByPath(self, s):
        bname = os.path.basename(s)
        if bname.endswith(".py"):
            return bname[:-3]
        if bname.endswith(".pyc"):
            return bname[:-4]

    def reload(self, targets=[]):
        if targets == []:
            self.logger.info("Reloading all exploits")
            self.loadAllExps()
            return

        #for e in targets:
        #    for ee in self.exps:
        #        if e == self.getExpNameByPath(ee.fname):
        #            self.logger.info("Reloading {exp}".format(exp=e))
        #            self.exps.remove(ee)
        #            self.exps.append(
        #                self.loadExp(e)
        #            )
        #            break
        for e in targets:
            for target in self.exps:
                l = self.exps[target]
                for ee in l:
                    if e == self.getExpNameByPath(ee.fname):
                        self.logger.info("Reloading {exp}".format(exp=e))
                        self.exps[target].remove(ee)
                        self.exps[target].append(
                            self.loadExp(e)
                        )
                    return

    def getExpByTarget(self, target):
        return self.exps[target] if target in self.exps else []
        ret = []
        for exp in self.exps:
            if exp.target == target:
                ret.append(exp)
        ret.sort(cmp=None, key=lambda x:x.level)
        return ret

