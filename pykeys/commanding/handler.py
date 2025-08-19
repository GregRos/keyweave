from typing import Any, Protocol

from pykeys.commanding.event import HotkeyEvent


class HotkeyHandler(Protocol):

    def __call__(self, event: HotkeyEvent, /) -> Any: ...
