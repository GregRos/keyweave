from functools import partial
from typing import Any

from pykeys.commanding.trigger_binding import CommandBinding, BindingInterceptor
from pykeys.layout.layout import Layout
from pykeys.schedulers.scheduling import Scheduler
from pykeys.layout_class.decorators import (
    get_func_hotkeys,
    get_func_metadata,
    is_interceptor,
)
from pykeys.schedulers.default import DefaultScheduler


def layout(name: str | None = None, scheduler: Scheduler | None = None):
    scheduler = scheduler or DefaultScheduler()

    def decorator(cls: type) -> Layout:
        interceptors: list[Any] = []
        layout = Layout(name or cls.__name__, scheduler=scheduler)
        # go over every method
        for key, handler in cls.__dict__.items():
            if not callable(handler):
                continue
            if is_interceptor(handler):
                interceptors.append(handler)
                continue
            hotkeys = get_func_hotkeys(handler)
            metadata = get_func_metadata(handler).default(label=key)
            has_self = "self" in handler.__code__.co_varnames
            if has_self:
                handler = partial(handler, cls)
            for trigger in hotkeys:
                layout += CommandBinding(
                    trigger,
                    handler,
                    metadata,
                )
        if layout.is_empty:
            raise ValueError(f"Layout {layout.name} is empty")
        for interceptor in interceptors:
            layout = layout.intercept(interceptor)
        return layout

    return decorator
