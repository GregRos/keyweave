from pykeys.key.key import Key
from pykeys.key.key_trigger import KeyTrigger
from pykeys.commanding.trigger_binding import CommandBinding


from typing import Iterator


class KeyBindingCollection:
    key: Key
    _map: dict[KeyTrigger, CommandBinding]

    def __init__(self, trigger: Key, bindings: dict[KeyTrigger, CommandBinding] = {}):
        self.key = trigger
        self._map = bindings

    def __getitem__(self, key: KeyTrigger) -> CommandBinding:
        return self._map[key]

    def set(self, binding: CommandBinding):
        return KeyBindingCollection(self.key, {**self._map, binding.trigger: binding})

    def __len__(self) -> int:
        return len(self._map)

    def __iter__(self) -> Iterator[CommandBinding]:
        return iter(self._map.values())

    def __add__(self, binding: CommandBinding):
        return self.set(binding)
