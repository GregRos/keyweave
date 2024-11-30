from dataclasses import dataclass, field
import inspect
from typing import Callable


from pykeys.commanding.event import KeyEvent
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
        if self._number_of_args != 2:
            raise ValueError(
                f"handler must accept 2 arguments, got {self._number_of_args}"
            )

    def map(self, handler_map: Callable[[Handler], Handler]) -> "CommandBinding":
        return CommandBinding(self.trigger, handler_map(self.handler), self.metadata)

    def __call__(self, event: KeyEvent, /):
        return self.handler(self.trigger, event)
