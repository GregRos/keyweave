from typing import Any, Protocol

from pykeys.handling.event import HotkeyEvent


class _HandlerA(Protocol):
    def __call__(self, info: HotkeyEvent, /) -> Any: ...


class _HandlerB(Protocol):

    def __call__(self, /) -> Any: ...


type Handler = _HandlerA | _HandlerB
