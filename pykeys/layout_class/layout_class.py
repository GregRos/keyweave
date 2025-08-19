from typing import Any

from pykeys.bindings.binding import Binding
from pykeys.layout.layout import Layout
from pykeys.schedulers.scheduling import Scheduler
from pykeys.layout_class.decorators import (
    get_func_hotkeys,
    get_func_metadata,
    is_interceptor,
)
from pykeys.util.func import maybe_bind_self


def layout(name: str | None = None, scheduler: Scheduler | None = None):

    def decorator(cls: type) -> Layout:
        interceptors: list[Any] = []
        layout = Layout(name or cls.__name__, scheduler=scheduler)
        # go over every method
        for key, handler in cls.__dict__.items():
            if not callable(handler):
                continue
            if is_interceptor(handler):
                interceptors.append(maybe_bind_self(handler, cls))
                continue
            hotkeys = get_func_hotkeys(handler)
            metadata = get_func_metadata(handler).default(label=key)
            for trigger in hotkeys:
                layout += Binding(
                    trigger,
                    metadata,
                )
        if layout.is_empty:
            raise ValueError(f"Layout {layout.name} is empty")
        for interceptor in interceptors:
            layout = layout.intercept(interceptor)
        return layout

    return decorator
