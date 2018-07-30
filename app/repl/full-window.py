#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from prompt_toolkit import PromptSession, AbortAction, Application, CommandLineInterface
from prompt_toolkit.document import Document
from prompt_toolkit.filters import has_focus
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import TextArea

class FrameApplication:
    STYLE = [
        ('output-field', 'bg:#000000 #FFFFFF'),
        ('input-field',  'bg:#000000 #FFFFFF'),
        ('line',         'bg:#00991C #FFFFFF')
    ]
    BANNER = """
        n0framework
        Powered by n0b0dy@eur3ka
    """

    def __init__(self):
        pass

    def parseline(self, s):
        return "Result of: " + s

    def start(self):
        # layout
        self.output_field = TextArea(
            style='class:output-field',
            text=BANNER,
            read_only=True,
            scrollbar=True
        )

        self.input_field = TextArea(
            height=1,
            prompt='>>> ',
            style='class:input-field'
        )

        self.container = HSplit([
            output_field,
            Window(height=1, char='-', style='class:line'),
            input_field
        ])

        # key bindings
        self.kb = KeyBindings()
        
        @kb.add('c-q')
        @kb.add('c-c')
        def _(event):
            event.app.exit()

        @kb.add('enter', filter=has_focus(input_field))
        def _(event):
            try:
                out = "\n\n[ In] {i}\n[Out]{o}".format(
                    i=self.input_field.text,
                    o=self.parseline(self.input_field.text)
                )
            except Exception as e:
                out = "\n\n{e}".format(e=e)
            new_out = self.output_field.text + out
            self.output_field.buffer.document = Document(
                text=new_text,
                cursor_position=len(new_text)
            )
            self.input_field.text = ''


        # style
        style = Style(self.LAYOUT_STYLE)

