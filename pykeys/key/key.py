from dataclasses import dataclass
from functools import total_ordering

type KeyInput = "str | Key"


@total_ordering
@dataclass(eq=True, match_args=True, init=False)
class Key:
    id: str

    def __init__(self, input: KeyInput):
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
        from pykeys.key.key_set import KeySet

        return KeySet({self, other})

    @property
    def down(self):
        from pykeys.key.key_trigger import Hotkey

        return Hotkey(self, "down")

    @property
    def up(self):
        from pykeys.key.key_trigger import Hotkey

        return Hotkey(self, "up")

    def __repr__(self) -> str:
        return f"[{self.id}]"

    def __str__(self) -> str:
        return repr(self)
