from pykeys.keys.key import Key
from pykeys.keys.key_trigger import KeyTrigger
from pykeys.keys.trigger_binding import TriggerBinding


from typing import Iterator


class KeyBindingCollection:
    key: Key
    _map: dict[KeyTrigger, TriggerBinding]

    def __init__(self, trigger: Key, bindings: dict[KeyTrigger, TriggerBinding] = {}):
        self.key = trigger
        self._map = bindings

    def __getitem__(self, key: KeyTrigger) -> TriggerBinding:
        return self._map[key]

    def set(self, binding: TriggerBinding):
        return KeyBindingCollection(self.key, {**self._map, binding.trigger: binding})

    def __len__(self) -> int:
        return len(self._map)

    def __iter__(self) -> Iterator[TriggerBinding]:
        return iter(self._map.values())

    def __add__(self, binding: TriggerBinding):
        return self.set(binding)
