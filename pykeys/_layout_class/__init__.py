from typing import Any, Protocol
from pykeys.interception import HotkeyInterceptionEvent
from pykeys.key_types import KeyInput

from pykeys.hotkey import Hotkey, HotkeyEvent
from abc import ABC
from functools import partial

from pykeys.bindings import Binding
from pykeys.commanding import CommandInfo
from pykeys._layout.layout import Layout
from pykeys.scheduling import Scheduler


class LayoutClass(ABC):

    def __intercept__(self, intercepted: HotkeyInterceptionEvent):
        pass

    def __new__(
        cls, name: str | None = None, scheduler: Scheduler | None = None
    ):
        obj = super().__new__(cls)
        layout = Layout(name or cls.__name__, scheduler=scheduler)
        for key in cls.__dict__.keys():
            # We need to get the attribute from the instance to apply
            # any __get__ decorators.
            binding = getattr(obj, key, None)
            match binding:
                case Binding() as b:
                    layout.add_binding(b)
                case CommandInfo() as c:
                    raise TypeError(f"Found unbound command: {c}")
                case _:
                    pass
        if "__intercept__" in cls.__dict__:
            intercept = cls.__dict__["__intercept__"]
            layout = layout.intercept(partial(intercept, obj))
        return layout


type TriggerInput = "Hotkey | KeyInput"


class InstHandler(Protocol):

    def __call__(self, other_self: Any, event: HotkeyEvent, /) -> Any: ...


class InstActionInterceptor(Protocol):

    def __call__(
        self, other_self: Any, action: HotkeyInterceptionEvent, /
    ) -> Any: ...
