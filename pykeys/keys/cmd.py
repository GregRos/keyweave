from dataclasses import dataclass, field
import inspect
from typing import Any, Protocol

from keyboard import KeyboardEvent
from time import time
from pykeys.keys.key_trigger import KeyTrigger


@dataclass()
class EventInfo:
    label: str
    description: str
    trigger: KeyTrigger
    timestamp: float = field(default_factory=lambda: time(), init=False)


class _HandlerA(Protocol):
    def __call__(self, info: EventInfo, /) -> None: ...


class _HandlerB(Protocol):
    def __call__(self, /) -> None: ...


type Handler = _HandlerA | _HandlerB


class Act:
    label: str
    handler: Handler
    description: str = ""
    _number_of_args: int

    def __init__(self, label: str, handler: Handler, description: str = ""):
        if not callable(handler):
            raise ValueError(f"handler must be a callable, got {handler}")
        self._number_of_args = len(inspect.signature(handler).parameters)
        if self._number_of_args not in (0, 1):
            raise ValueError(
                f"handler must accept 0 or 1 arguments, got {self._number_of_args}"
            )
        self.label = label
        self.handler = handler
        self.description = description

    def __call__(self, trigger: KeyTrigger) -> None:
        handler: Any = self.handler
        info = EventInfo(
            label=self.label,
            description=self.description,
            trigger=trigger,
        )
        match self._number_of_args:
            case 0:
                return handler()
            case 1:
                return handler(info)
            case _:
                ...
