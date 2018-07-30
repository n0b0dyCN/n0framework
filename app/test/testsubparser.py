import argparse

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help="sub-command help", dest="service")

pa = subparsers.add_parser("submitter", help="submitter help")
pa.add_argument("action", type=str, help="action to submitter")

pb = subparsers.add_parser("gamebox", help="gamebox help")
pb.add_argument("action", type=str, help="action to gamebox")

args = parser.parse_args()
import pprint
pprint.pprint(args)
pprint.pprint(args.service)
