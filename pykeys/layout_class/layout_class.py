from functools import partial

from pykeys.handling.trigger_binding import TriggerBinding
from pykeys.layout.layout import Layout
from pykeys.schedulers.scheduling import Scheduler
from pykeys.layout_class.decorators import get_func_hotkeys, get_func_metadata
from pykeys.schedulers.default import DefaultScheduler


def hotkey_layout(name: str | None = None, scheduler: Scheduler | None = None):
    scheduler = scheduler or DefaultScheduler()

    def decorator(cls: type) -> Layout:
        layout = Layout(name or cls.__name__, scheduler=scheduler)
        # go over every method
        for key, handler in cls.__dict__.items():
            if not callable(handler):
                continue
            hotkeys = get_func_hotkeys(handler)
            metadata = get_func_metadata(handler).default(label=key)
            has_self = "self" in handler.__code__.co_varnames
            if has_self:
                handler = partial(handler, cls)
            for trigger in hotkeys:
                layout += TriggerBinding(
                    trigger,
                    handler,
                    metadata,
                )
        if layout.is_empty:
            raise ValueError(f"Layout {layout.name} is empty")
        return layout

    return decorator
