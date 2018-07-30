from . import command
from . import command_register

from .test import test_command
from .general import help_command
from .general import exit_command
from .general import service_command
from .general import attack_command

__all__ = [
    'command',
    'registry',
    'test_command',

    # general
    'help_command',
    'exit_command',
    'service_command'
    'attack_command'
]
