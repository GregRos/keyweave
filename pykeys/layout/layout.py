from typing import Iterable
import keyboard

from pykeys.bindings.binding_collection import BindingCollection
from pykeys.keys.trigger_binding import TriggerBinding
from pykeys.layout.key_hook import KeyHook


# KEY | MODIFIERS
#
class Layout:
    _registered: list[KeyHook]
    _map: BindingCollection

    def __init__(self, name: str, bindings: Iterable[TriggerBinding] = ()):
        self.name = name
        for binding in bindings:
            self.add_binding(binding)

    def __iadd__(self, binding: TriggerBinding):
        self.add_binding(binding)
        return self

    def add_binding(self, binding: TriggerBinding):
        self._map += binding

    def __len__(self):
        return len(self._map)

    def __iter__(self):
        return iter(self._map)

    def _get_key_hooks(self):
        return [KeyHook(key, bindings) for key, bindings in self._map.pairs]

    def __enter__(self):
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
