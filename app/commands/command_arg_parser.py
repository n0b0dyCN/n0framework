import argparse

class ParserExitException(BaseException):
    pass

class CommandArgParser(argparse.ArgumentParser):
    def exit(self, _status=0, _message=None):
        raise ParserExitException()

    def error(message):
        return
