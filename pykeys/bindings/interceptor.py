from dataclasses import dataclass
from typing import Protocol
from pykeys.commanding.event import HotkeyEvent
from pykeys.commanding.handler import HotkeyHandler


@dataclass(init=False)
class InterceptedHotkey(HotkeyEvent):
    _handled: bool = False

    def __init__(self, event: HotkeyEvent, handler: HotkeyHandler):
        HotkeyEvent.__init__(self, event.hotkey, event.event, event.command)
        self._handler = handler

    def next(self):
        self._handled = True
        result = self._handler(self)
        return result

    def end(self):
        self._handled = True

    @property
    def handled(self):
        return self._handled


class HotkeyInterceptor(Protocol):
    def __call__(self, action: InterceptedHotkey): ...
