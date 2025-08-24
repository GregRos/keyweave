from curses.ascii import ismeta
import inspect
from typing import Any

from pykeys.commanding.command import Command
from pykeys.commanding.handler import FuncHotkeyHandler, HotkeyHandler
from pykeys.commanding.event import HotkeyEvent
from pykeys.layout.layout import Layout


def commandx[T: None | Layout](
    label: str | None = None, description: str | None = None
):
    class commandx(Command):
        def __init__(self, func: HotkeyHandler):
            self.func = func
            super().__init__(
                label or func.__qualname__, self._call, description=description
            )

        def _call(self, event: HotkeyEvent, /):
            if inspect.ismethod(self.func):
                raise TypeError(
                    f"Expected __get__ to be called when decorating instance method '{self.func.__qualname__}'"
                )
            return self.func(event)  # type: ignore

        def _make(self, instance: T | None = None):

            def wrapper(event: HotkeyEvent, /) -> Any:
                if inspect.ismethod(self.func):
                    return self.func.__get__(instance)(event)
                return self.func(event)  # type: ignore

            _label = label or self.func.__qualname__
            return Command(_label, wrapper, description=description)

        def __get__(self, instance: T | None, owner: type[T] | None = None):
            return self._make(instance)

    def deco(func: HotkeyHandler):
        return commandx(func)

    return deco
