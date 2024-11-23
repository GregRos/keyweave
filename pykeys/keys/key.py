from dataclasses import dataclass
from functools import total_ordering
from pprint import pp


@total_ordering
@dataclass(eq=True, order=True, match_args=True, frozen=True)
class Key:
    id: str

    @property
    def label(self):
        return self.id

    @property
    def is_numpad(self):
        return self.id.startswith("num ")

    def __hash__(self) -> int:
        return hash(self.id)

    @property
    def is_mouse(self):
        return self.id.startswith("mouse ")

    @property
    def is_keyboard(self):
        return not self.is_mouse

    def __lt__(self, other: "Key") -> bool:
        return self.id < other.id

    @property
    def specificity(self):
        return 1

    def __add__(self, other: "Key"):
        from pykeys.keys.key_set import KeySet

        return KeySet({self, other})

    @property
    def down(self):
        from pykeys.keys.key_trigger import KeyTrigger

        return KeyTrigger(self, "down")

    @property
    def up(self):
        from pykeys.keys.key_trigger import KeyTrigger

        return KeyTrigger(self, "up")

    def __repr__(self) -> str:
        return self.id

    def __str__(self) -> str:
        return self.id
