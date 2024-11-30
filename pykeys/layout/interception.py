from dataclasses import dataclass
from typing import Protocol
from pykeys.commanding.event import KeyEvent
from pykeys.commanding.handler import Handler
from pykeys.key.key_trigger import KeyTrigger


@dataclass(init=False)
class InterceptedAction:
    _handled: bool = False
    event: KeyEvent
    trigger: KeyTrigger

    def __init__(self, trigger: KeyTrigger, event: KeyEvent, handler: Handler):
        self.trigger = trigger
        self.event = event
        self._handler = handler

    def run(self):
        self._handled = True
        self._handler(self.trigger, self.event)

    def skip(self):
        self._handled = True

    @property
    def handled(self):
        return self._handled


class ActionInterceptor(Protocol):
    def __call__(self, action: InterceptedAction): ...
