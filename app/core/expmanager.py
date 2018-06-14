import prettytable
import os
import imp

from .util import safeGetAttr, getLog

class ExpManager:
    def __init__(self, exppath):
        self.exppath = exppath
        self.exps = []

    def getExps(self):
        explist = []
        for f in os.listdir(self.exppath):
            if os.path.isfile(self.exppath + os.sep + f):
                if f[-3:] == ".py":
                    explist.append(f[:-3])
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
            return obj 
        except Exception as e:
            msg = "Cannot load exploit `{exp_name}`".format(exp_name=exp_name)
            return None

    def loadAllExps(self):
        self.exps = []
        exists_exps = self.getExps()
        ret = []
        for exists_exp in exists_exps:
            e = self.loadExp(exists_exp)
            if e != None:
                ret.append(e)
        self.exps = ret

    def printExps(self):
        x = lambda x,y: safeGetAttr(x,y)
        pt = prettytable.PrettyTable(["file", "target", "author", "level", "timeout"])
        for exp in self.exps:
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

    def reload(self, target=[]):
        if target == []:
            self.loadAllExps()
            return

        for e in target:
            for ee in self.exps:
                if e == self.getExpNameByPath(ee.fname):
                    self.exps.remove(ee)
                    self.exps.append(
                        self.loadExp(e)
                    )
                    break

    def getExpByTarget(self, target):
        ret = []
        for exp in self.exps:
            if exp.target == target:
                ret.append(exp)
        ret.sort(cmp=None, key=lambda x:x.level)
        return ret

