from dataclasses import dataclass, field
import inspect
from typing import Any, Protocol, Self

from time import time
from pykeys.keys.metadata import HotkeyMetadata
from pykeys.keys.key_trigger import KeyTrigger


@dataclass()
class EventInfo(HotkeyMetadata):
    trigger: KeyTrigger
    timestamp: float = field(default_factory=lambda: time(), init=False)


class _HandlerA(Protocol):
    def __call__(self, info: EventInfo, /) -> Any: ...


class _HandlerB(Protocol):

    def __call__(self, /) -> Any: ...


type Handler = _HandlerA | _HandlerB


class Act:
    handler: Handler
    metadata: HotkeyMetadata
    _number_of_args: int

    def __init__(self, metadata: HotkeyMetadata, handler: Handler):
        if not callable(handler):
            raise ValueError(f"handler must be a callable, got {handler}")
        self._number_of_args = len(inspect.signature(handler).parameters)
        if self._number_of_args not in (0, 1):
            raise ValueError(
                f"handler must accept 0 or 1 arguments, got {self._number_of_args}"
            )
        self.metadata = metadata
        self.handler = handler

    def __call__(self, trigger: KeyTrigger) -> None:
        handler: Any = self.handler
        info = EventInfo(
            label=self.metadata.label,
            description=self.metadata.description,
            trigger=trigger,
        )
        match self._number_of_args:
            case 0:
                return handler()
            case 1:
                return handler(info)
            case _:
                ...
