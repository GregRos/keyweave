from dataclasses import dataclass, field
import inspect
from typing import Any


from pykeys.commanding.event import CommandEvent
from pykeys.commanding.handler import Handler
from pykeys.key.key_trigger import KeyTrigger
from pykeys.commanding.metadata import Command


@dataclass(match_args=True)
class CommandBinding:
    trigger: KeyTrigger
    handler: Handler
    metadata: Command
    _number_of_args: int = field(init=False)

    def __post_init__(self):
        self._number_of_args = len(inspect.signature(self.handler).parameters)
        if not callable(self.handler):
            raise ValueError(f"handler must be a callable, got {self.handler}")
        if self._number_of_args not in (0, 1):
            raise ValueError(
                f"handler must accept 0 or 1 arguments, got {self._number_of_args}"
            )

    def __call__(self) -> None:
        handler: Any = self.handler
        info = CommandEvent(
            label=self.metadata.label,
            description=self.metadata.description,
            trigger=self.trigger,
        )
        match self._number_of_args:
            case 0:
                return handler()
            case 1:
                return handler(info)
            case _:
                ...
