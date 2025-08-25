from dataclasses import dataclass
from functools import total_ordering
from typing import TYPE_CHECKING

from pykeys.key.key_event_type import KeyEventType

if TYPE_CHECKING:
    from key_set import KeySet
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

    def __and__(self, other: "Key | KeySet"):

        return self.down.modifiers(other)

    @property
    def down(self):
        from pykeys.key.hotkey import Hotkey, HotkeyInfo

        return Hotkey(HotkeyInfo(trigger=self, type=KeyEventType("down")))

    @property
    def up(self):
        from pykeys.key.hotkey import Hotkey, HotkeyInfo

        return Hotkey(HotkeyInfo(trigger=self, type=KeyEventType("up")))

    def __repr__(self) -> str:
        return f"[{self.id}]"

    def __str__(self) -> str:
        return repr(self)
