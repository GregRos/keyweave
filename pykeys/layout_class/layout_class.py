from abc import ABC
from functools import partial

from pykeys.bindings.binding import Binding
from pykeys.bindings.interceptor import InterceptedHotkey
from pykeys.commanding.command import AbsCommand
from pykeys.layout.layout import Layout
from pykeys.schedulers.scheduling import Scheduler


class LayoutClass(ABC):

    def __intercept__(self, intercepted: InterceptedHotkey):
        pass

    def __new__(cls, name: str | None = None, scheduler: Scheduler | None = None):
        obj = super().__new__(cls)
        layout = Layout(name or cls.__name__, scheduler=scheduler)
        for key in cls.__dict__.keys():
            # We need to get the attribute from the instance to apply
            # any __get__ decorators.
            binding = getattr(obj, key, None)
            match binding:
                case Binding() as b:
                    layout.add_binding(b)
                case AbsCommand() as c:
                    raise TypeError(f"Found unbound command: {c}")
                case _:
                    pass
        if "__intercept__" in cls.__dict__:
            intercept = cls.__dict__["__intercept__"]
            layout = layout.intercept(partial(intercept, obj))
        return layout
