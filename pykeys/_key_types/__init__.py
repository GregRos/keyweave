from functools import total_ordering
from typing import Iterable, Literal


TriggerTypeName = Literal["down", "up"]


@total_ordering
class KeyEventType:
    __match_args__ = ("name",)

    def __init__(self, name: "TriggerTypeName | KeyEventType"):
        self.name = name if isinstance(name, str) else name.name

    def __hash__(self) -> int:
        return hash(self.name)

    @property
    def char(self) -> str:
        return "↓" if self.name == "down" else "↑"

    def __eq__(self, other: object) -> bool:
        match other:
            case KeyEventType(other_name):
                return self.name == other_name
            case str(s):
                return self.name == s
            case _:
                return False

    def __lt__(self, other: "KeyEventType") -> bool:
        return self.name < other.name


@total_ordering
class Key:
    id: str

    def __init__(self, input: "str | Key"):
        self.id = input if isinstance(input, str) else input.id

    @property
    def label(self):
        return self.id

    @property
    def is_numpad(self):
        return self.id.startswith("num:")

    def __hash__(self) -> int:
        return hash(self.id)

    @property
    def is_mouse(self):
        return self.id.startswith("mouse:")

    @property
    def is_keyboard(self):
        return not self.is_mouse

    def __lt__(self, other: "Key") -> bool:
        return self.id < other.id

    @property
    def specificity(self):
        return 1

    def __add__(self, other: "Key"):
        from pykeys._key_types import KeySet

        return KeySet({self, other})

    def __and__(self, other: "Key | KeySet"):
        return self.down.modifiers(other)

    @property
    def down(self):
        from pykeys._hotkey import Hotkey, HotkeyInfo

        return Hotkey(HotkeyInfo(trigger=self, type=KeyEventType("down")))

    @property
    def up(self):
        from pykeys._hotkey import Hotkey, HotkeyInfo

        return Hotkey(HotkeyInfo(trigger=self, type=KeyEventType("up")))

    def __repr__(self) -> str:
        return f"[{self.id}]"

    def __str__(self) -> str:
        return repr(self)


type KeyInput = "str | Key"


from typing import Union

KeysInput = Union["Key", "KeySet", Iterable[Key]]


@total_ordering
class KeySet:
    __match_args__ = ("set",)
    set: frozenset[Key]

    def __init__(self, input: KeysInput = {}):
        match input:
            case Key():
                self.set = frozenset({input})
            case KeySet():
                self.set = input.set
            case _:
                self.set = frozenset(input)

    def __hash__(self) -> int:
        return hash(self.set)

    def __bool__(self) -> bool:
        return bool(self.set)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, KeySet) and self.set == other.set

    def __lt__(self, other: "KeySet") -> bool:
        return self.set < other.set

    def __add__(self, other: KeysInput) -> "KeySet":
        return KeySet(self.set | KeySet(other).set)

    @property
    def specificity(self) -> int:
        return sum(key.specificity for key in self.set)

    def __iter__(self):
        return iter(self.set)

    def __contains__(self, key: Key) -> bool:
        return key in self.set

    def __len__(self) -> int:
        return len(self.set)

    def __repr__(self) -> str:
        if not self.set:
            return ""
        joined = " + ".join(repr(key) for key in self.set)
        return joined

    def __str__(self) -> str:
        return repr(self)


__all__ = [
    "Key",
    "KeySet",
    "KeyInput",
    "KeysInput",
    "KeyEventType",
    "TriggerTypeName",
]
