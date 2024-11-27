from typing import Any, Iterable, Iterator, overload

from pykeys.key.key import Key
from pykeys.key.key_trigger import KeyTrigger
from pykeys.commanding.trigger_binding import CommandBinding
from pykeys.bindings.key_binding_collection import KeyBindingCollection


class BindingCollection(Iterable[KeyBindingCollection]):
    _map: dict[Key, KeyBindingCollection]
    _handler_map: dict[Key, Any]

    def __init__(self, input: dict[Key, KeyBindingCollection] = {}):
        self._map = input

    def __add__(self, input: CommandBinding):
        trigger_key = input.trigger.trigger
        new_map = self._map.copy()
        trigger_collection = new_map.get(trigger_key, KeyBindingCollection(trigger_key))
        trigger_collection = trigger_collection.set(input)
        new_map[trigger_key] = trigger_collection
        return BindingCollection(new_map)

    @property
    def keys(self) -> set[Key]:
        return set(self._map.keys())

    @property
    def pairs(self) -> Iterable[tuple[Key, KeyBindingCollection]]:
        return self._map.items()

    @overload
    def __getitem__(self, key: Key) -> KeyBindingCollection: ...

    @overload
    def __getitem__(self, key: KeyTrigger) -> CommandBinding: ...

    def __getitem__(
        self, key: Key | KeyTrigger
    ) -> KeyBindingCollection | CommandBinding:
        match key:
            case Key():
                return self._map[key]
            case KeyTrigger():
                return self._map[key.trigger][key]

    def __iter__(self) -> Iterator[KeyBindingCollection]:
        return iter(self._map.values())

    def __len__(self) -> int:
        return len(self._map)

    def __repr__(self) -> str:
        return repr(self._map)
