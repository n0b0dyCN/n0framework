from __future__ import unicode_literals
import sys

from prompt_toolkit.completion import WordCompleter

from ..command import Command
from ..command_arg_parser import CommandArgParser

class ServiceCommand(Command):
    def __init__(self):
        pass

    def name(self):
        return "service"

    def description(self):
        return "Service Control command"

    def action(self, args=None, **kwargs):
        if "serviceReg" not in kwargs:
            msg = "No service register provided."
            return
        serv = args.serv_name
        act = args.action
        kwargs["serviceReg"].handleReq(serv, act)

    def make_parser(self, **kwargs):
        # using subparser
        parser = CommandArgParser()
        subparsers = parser.add_subparsers(dest="serv_name", help="service name")
        if "serviceReg" not in kwargs:
            msg = "serviceReg needed to build parser for `service` command"
            return None
        for serv in kwargs["serviceReg"].services():
            serv.make_parser(subparsers)
        p_all = subparsers.add_parser("all", help="For all services")
        p_all.add_argument("action", type=str, help="action to all services")
        return parser


    def make_completer(self, **kwargs):
        if "serviceReg" in kwargs:
            l = kwargs["serviceReg"].names()
            l.append("all")
            return WordCompleter(l)


