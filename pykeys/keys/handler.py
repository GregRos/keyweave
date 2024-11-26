from typing import Any, Protocol

from pykeys.keys.event import HotkeyEvent


class _HandlerA(Protocol):
    def __call__(self, info: HotkeyEvent, /) -> Any: ...


class _HandlerB(Protocol):

    def __call__(self, /) -> Any: ...


type Handler = _HandlerA | _HandlerB
