from functools import partial
from typing import Any, Callable, NotRequired, TypedDict

from pykeys.keys.cmd import Act
from pykeys.keys.trigger_binding import TriggerBinding
from pykeys.layout.layout import Layout
from pykeys.layout.scheduling import Scheduler
from pykeys.layout_class.decorators import get_func_hotkeys, get_func_metadata
from pykeys.schedulers.thread_pool import DefaultScheduler


class LayoutOptions(TypedDict):
    name: NotRequired[str]
    description: NotRequired[str]
    scheduler: NotRequired[Scheduler]


def hotkey_layout(
    name: str | None = None, scheduler: Scheduler | None = None, description: str = ""
):
    scheduler = scheduler or DefaultScheduler()

    def decorator(cls: type) -> Layout:
        layout = Layout(
            name or cls.__name__,
            scheduler=scheduler,
            description=description,
        )
        # go over every method
        for key, value in cls.__dict__.items():
            if not callable(value):
                continue
            hotkeys = get_func_hotkeys(value)
            metadata = get_func_metadata(value).default(label=key)
            has_self = "self" in value.__code__.co_varnames
            if has_self:
                value = partial(value, cls)
            for trigger in hotkeys:
                layout += TriggerBinding(
                    trigger,
                    Act(
                        handler=value,
                        metadata=metadata,
                    ),
                )
        if layout.is_empty:
            raise ValueError(f"Layout {layout.name} is empty")
        return layout

    return decorator
