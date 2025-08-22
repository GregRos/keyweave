from typing import Any, Protocol

from pykeys.commanding.event import HotkeyEvent


class FuncHotkeyHandler(Protocol):

    def __call__(self, event: HotkeyEvent, /) -> Any: ...


class MethodHotkeyHandler(Protocol):
    def __call__(self, instance: Any, event: HotkeyEvent, /) -> Any: ...


type HotkeyHandler = FuncHotkeyHandler | MethodHotkeyHandler
