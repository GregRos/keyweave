from dataclasses import dataclass
from typing import Protocol
from pykeys.commanding.event import TriggeredKeyEvent
from pykeys.commanding.handler import Handler


@dataclass(init=False)
class InterceptedAction:
    _handled: bool = False
    event: TriggeredKeyEvent

    def __init__(self, event: TriggeredKeyEvent, handler: Handler):
        self.event = event
        self._handler = handler

    def next(self):
        self._handled = True
        self._handler(self.event)

    def end(self):
        self._handled = True

    @property
    def handled(self):
        return self._handled


class ActionInterceptor(Protocol):
    def __call__(self, action: InterceptedAction): ...
