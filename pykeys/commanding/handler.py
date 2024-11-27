from typing import Any, Protocol

from pykeys.commanding.event import CommandEvent


class _HandlerA(Protocol):
    def __call__(self, info: CommandEvent, /) -> Any: ...


class _HandlerB(Protocol):

    def __call__(self, /) -> Any: ...


type Handler = _HandlerA | _HandlerB
