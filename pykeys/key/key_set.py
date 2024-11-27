from functools import total_ordering
from typing import Iterable

from pykeys.key.key import Key

type KeysInput = Key | KeySet | Iterable[Key]


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
    def specificity(self):
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
