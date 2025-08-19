from pykeys.key.key import Key, KeyInput
from pykeys.key.key_set import KeySet, KeysInput
from pykeys.key.key_event_type import KeyEventType, TriggerTypeName


class Hotkey:
    __match_args__ = ("key", "type", "modifiers")
    trigger: Key
    type: KeyEventType
    modifiers: KeySet

    def __init__(
        self,
        key: KeyInput,
        type: TriggerTypeName | KeyEventType,
        modifiers: KeysInput = set(),
    ):
        self.trigger = Key(key)
        self.type = KeyEventType(type)
        self.modifiers = KeySet(modifiers)

    @property
    def trigger_label(self) -> str:
        return f"{self.type.char} {self.trigger}"

    def __hash__(self) -> int:
        return hash((self.trigger, self.type, self.modifiers))

    @property
    def is_down(self) -> bool:
        return self.type == "down"

    @property
    def is_up(self) -> bool:
        return self.type == "up"

    def __lt__(self, other: "Hotkey") -> bool:
        return (self.trigger, self.type, self.modifiers) < (
            other.trigger,
            other.type,
            other.modifiers,
        )

    def __and__(self, other: KeysInput):
        return self.with_modifiers(other)

    def with_modifiers(self, modifiers: KeysInput):
        return Hotkey(self.trigger, self.type, self.modifiers + modifiers)

    def __repr__(self) -> str:
        if not self.modifiers:
            return f"{self.trigger_label}"
        else:
            return f"{self.trigger_label} & {self.modifiers}"

    def __str__(self) -> str:
        return repr(self)

    @property
    def specificity(self):
        return self.trigger.specificity + self.modifiers.specificity
