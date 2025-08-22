import inspect
from typing import Any

from pykeys.commanding.command import Command
from pykeys.commanding.handler import FuncHotkeyHandler, HotkeyHandler
from pykeys.commanding.event import HotkeyEvent
from pykeys.layout.layout import Layout


def commandx[T: None | Layout](
    label: str | None = None, description: str | None = None
):
    class commandx:
        def __init__(self, func: HotkeyHandler):
            self.func = func

        def _make(self, instance: T | None):
            sig = inspect.signature(self.func)
            arg_count = len(sig.parameters)

            def wrapper(event: HotkeyEvent, /) -> Any:
                if arg_count == 1:
                    return self.func(event)  # type: ignore
                elif arg_count == 2:
                    return self.func(instance, event)  # type: ignore

            _label = label or self.func.__qualname__
            return Command(_label, wrapper, description=description)

        def __get__(self, instance: T | None, owner: type[T] | None = None):
            return self._make(instance)

    def deco(func: HotkeyHandler):
        return commandx(func)

    return deco
