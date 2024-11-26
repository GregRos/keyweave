from typing import Iterable

from pykeys.bindings.binding_collection import BindingCollection
from pykeys.keys.trigger_binding import TriggerBinding
from pykeys.layout.key_hook import KeyHook
from pykeys.layout.scheduling import Scheduler


# KEY | MODIFIERS
#
class Layout:
    _registered: list[KeyHook]
    _map: BindingCollection
    _active: bool = False

    def __init__(
        self, name: str, scheduler: Scheduler, bindings: Iterable[TriggerBinding] = ()
    ):
        self.name = name
        self._scheduler = scheduler
        self._map = BindingCollection()
        for binding in bindings:
            self.add_binding(binding)

    def __iadd__(self, binding: TriggerBinding):
        self.add_binding(binding)
        return self

    @property
    def is_empty(self):
        return len(self._map) == 0

    @property
    def active(self):
        return self._active

    def add_binding(self, binding: TriggerBinding):
        self._map += binding

    def __len__(self):
        return len(self._map)

    def __iter__(self):
        return iter(self._map)

    def _get_key_hooks(self):
        return [
            KeyHook(key, bindings, self._scheduler) for key, bindings in self._map.pairs
        ]

    def __enter__(self):
        from .print_layout import get_layout_table

        print(f"➡️ {get_layout_table(self)}")
        key_hooks = self._get_key_hooks()
        registered: list[KeyHook] = []
        try:
            for hook in key_hooks:
                hook.__enter__()
                registered.append(hook)
        except:
            for hook in registered:
                hook.__exit__()
            raise
        self._registered = key_hooks

    def __exit__(self):
        for hook in self._registered:
            hook.__exit__()
