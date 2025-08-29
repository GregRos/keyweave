from functools import total_ordering
from typing import Iterable, Literal


@total_ordering
class Key:
    """
    Represents a single keyboard, mouse, or controller key input. You can access a preset list of
    these events via the `pykeys.key` import, for example:

    >>> from pykeys import key
    >>> key.a # represents the "a" key

    Otherwise, you can use this class to reference keys using a string:

    >>> Key("a") # also represents the "a" key

    - For mouse keys, use `Key("mouse:1")` through `Key("mouse:5")` for buttons 1-5.
    - For numpad keys, use `Key("num:0")` through `Key("num:9")` for keys 0-9.

    For symbol keys, use:

    >>> Key("+") # the + key
    >>> Key("num:+") # the + key on the numpad

    Key objects are comparable, hashable, and equatable.
    """

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

    def __invert__(self):
        return KeyInputState(self, "up")

    @property
    def is_mouse(self):
        """
        Whether this key is a mouse key.
        """
        return self.id.startswith("mouse:")

    @property
    def is_keyboard(self):
        """
        Whether this key is a keyboard key.
        """
        return not self.is_mouse

    def __lt__(self, other: "Key") -> bool:
        return self.id < other.id

    @property
    def specificity(self):
        return 1

    def __add__(self, other: "Key | KeyInputState"):
        """
        Combines two keys into a `KeySet`, an unordered collection of keys.
        """
        from pykeys.key_types import KeySet

        return KeySet({self, other})

    def __and__(self, other: "KeysInput"):
        """
        Creates a Hotkey using the left key as a trigger (down event) and the right keys as modifiers.

        >>> from pykeys import key
        >>> hotkey = key.a & key.ctrl + key.shift
        >>> hotkey2 = key.a & [key.ctrl, key.shift]
        >>> hotkey3 = key.a & key.ctrl
        """
        return self.down.modifiers(other)

    @property
    def down(self) -> "KeyInputState":

        return KeyInputState(self, "down")

    @property
    def up(self):
        return KeyInputState(self, "up")

    def __repr__(self) -> str:
        return f"{self.id}"

    def __str__(self) -> str:
        return repr(self)


type TriggerTypeName = Literal["down", "up"]


@total_ordering
class KeyInputState:
    """
    Represents key up or key down states.
    """

    __match_args__ = ("key", "state")

    def __str__(self) -> str:
        """
        A label for the Hotkey's trigger key.
        """
        return f"{self.state_char}{self.key}"

    def __repr__(self) -> str:
        return str(self)

    def __invert__(self):
        return KeyInputState(self.key, "up" if self.is_down else "down")

    def __init__(self, key: Key, state: TriggerTypeName):
        self.key = key
        self.state = state

    def __hash__(self) -> int:
        return hash(self.key) ^ hash(self.state)

    def modifiers(self, modifiers: "KeysInput"):
        from ..hotkey import Hotkey, HotkeyInfo

        """
        Adds modifiers to a Hotkey.
        """
        return Hotkey(
            HotkeyInfo(
                trigger=self,
                modifiers=KeySet(modifiers),
                passthrough=False,
            )
        )

    def __add__(self, other: "KeyInputState | Key"):
        """
        Combines two keys into a `KeySet`, an unordered collection of keys.
        """
        from pykeys.key_types import KeySet

        return KeySet({self, other})

    @property
    def state_char(self) -> str:
        return "↓" if self.state == "down" else "↑"

    def __lt__(self, other: "KeyInputState") -> bool:
        return self.key < other.key and self.state < other.state

    @property
    def specificity(self) -> int:
        return self.key.specificity

    @property
    def is_down(self) -> bool:
        return self.state == "down"

    @property
    def is_up(self) -> bool:
        return self.state == "up"


type KeyInput = "str | Key"

type KeyStateInput = Key | KeyInputState
type KeysInput = KeyInputState | KeySet | Key | Iterable[Key | KeyInputState]


def resolve_key_input(k: Key | KeyInputState) -> KeyInputState:
    match k:
        case Key():
            return KeyInputState(k, "down")
        case KeyInputState():
            return k
        case _:
            raise TypeError(f"Invalid key input: {k}")


@total_ordering
class KeySet:
    """
    An unordered collection of `KeyInputState` objects, used as a set of modifiers.
    """

    __match_args__ = ("set",)
    set: frozenset[KeyInputState]

    def __invert__(self):
        return KeySet(key.__invert__() for key in self.set)

    def __init__(self, input: KeysInput = {}):
        match input:
            case Key() | KeyInputState():
                self.set = frozenset({resolve_key_input(input)})
            case KeySet():
                self.set = input.set
            case _:
                self.set = frozenset(resolve_key_input(x) for x in input)

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

    def __contains__(self, key: Key | KeyInputState) -> bool:
        return resolve_key_input(key) in self.set

    def __len__(self) -> int:
        return len(self.set)

    def __repr__(self) -> str:
        if not self.set:
            return ""
        joined = " + ".join(repr(key) for key in self.set)
        return joined

    def __str__(self) -> str:
        return repr(self)
