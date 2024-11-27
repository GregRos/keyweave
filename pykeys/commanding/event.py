from pykeys.key.key_trigger import KeyTrigger
from pykeys.commanding.metadata import Command


from dataclasses import dataclass, field
from time import time


@dataclass()
class CommandEvent(Command):
    trigger: KeyTrigger
    timestamp: float = field(default_factory=lambda: time(), init=False)
