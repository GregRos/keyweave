from functools import total_ordering
from typing import Iterable, Literal


TriggerTypeName = Literal["down", "up"]


@total_ordering
class KeyEventType:
    """
    Represents key up or key down states.
    """

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

    def __add__(self, other: "Key"):
        """
        Combines two keys into a `KeySet`, an unordered collection of keys.
        """
        from pykeys.key_types import KeySet

        return KeySet({self, other})

    def __and__(self, other: "Iterable[Key] | Key | KeySet"):
        """
        Creates a Hotkey using the left key as a trigger (down event) and the right keys as modifiers.

        >>> from pykeys import key
        >>> hotkey = key.a & key.ctrl + key.shift
        >>> hotkey2 = key.a & [key.ctrl, key.shift]
        >>> hotkey3 = key.a & key.ctrl
        """
        return self.down.modifiers(other)

    @property
    def down(self):
        """
        Returns a Hotkey for the key being pressed down.
        """
        from pykeys.hotkey import Hotkey, HotkeyInfo

        return Hotkey(HotkeyInfo(trigger=self, type=KeyEventType("down")))

    @property
    def up(self):
        """
        Returns a Hotkey for the key being released.
        """
        from pykeys.hotkey import Hotkey, HotkeyInfo

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
    """
    An unordered collection of `Key` objects, used as a set of modifiers.
    """

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
