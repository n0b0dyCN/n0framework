
from prompt_toolkit.completion import WordCompleter
from .util import parseline

class Completer(WordCompleter):
    def __init__(self, words, meta_dict, commandReg, serviceReg):
        self.__commandReg = commandReg
        self.__serviceReg = serviceReg
        self.__completers = {}
        super(Completer, self).__init__(words, meta_dict=meta_dict, ignore_case=True)

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor.lstrip()
        if ' ' in text:
            cmd, args = parseline(text)
            completer = None
            if cmd in self.__completers:
                completer = self.__completers[cmd]
            else:
                completer = self.__commandReg.getCompleter(cmd,
                                                           commandReg=self.__commandReg,
                                                           serviceReg=self.__serviceReg
                                                          )
                self.__completers[cmd] = completer
            if not completer:
                return []
            return completer.get_completions(document, complete_event)
        return super(Completer, self).get_completions(document, complete_event)

