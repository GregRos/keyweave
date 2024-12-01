from pykeys.key.key import Key
from pykeys.key.hotkey import Hotkey
from pykeys.bindings.binding import Binding


from typing import Iterator


class KeyBindingCollection:
    key: Key
    _map: dict[Hotkey, Binding]

    def __init__(self, trigger: Key, bindings: dict[Hotkey, Binding] = {}):
        self.key = trigger
        self._map = bindings

    def __getitem__(self, key: Hotkey) -> Binding:
        return self._map[key]

    def set(self, binding: Binding):
        return KeyBindingCollection(self.key, {**self._map, binding.hotkey: binding})

    def __len__(self) -> int:
        return len(self._map)

    def __iter__(self) -> Iterator[Binding]:
        return iter(self._map.values())

    def __add__(self, binding: Binding):
        return self.set(binding)
