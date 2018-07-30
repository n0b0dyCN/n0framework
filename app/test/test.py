from __future__ import unicode_literals

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter

c = WordCompleter(['aaa', 'bbb', 'bbc'])
p = PromptSession(message='>>> ', completer=c)
while True:
    print p.prompt()
