from typing import TYPE_CHECKING
from pykeys.keys.key import Key
from pykeys.keys.key_set import KeySet, KeysInput
from pykeys.keys.trigger_type import TriggerType, TriggerTypeName

if TYPE_CHECKING:
    from pykeys.keys.cmd import Act


class KeyTrigger:
    __match_args__ = ("key", "type", "modifiers")
    trigger: Key
    type: TriggerType
    modifiers: KeySet

    def __init__(
        self,
        key: Key,
        type: TriggerTypeName | TriggerType,
        modifiers: KeysInput = set(),
    ):
        self.trigger = key
        self.type = TriggerType(type)
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

    def __lt__(self, other: "KeyTrigger") -> bool:
        return (self.trigger, self.type, self.modifiers) < (
            other.trigger,
            other.type,
            other.modifiers,
        )

    def __and__(self, other: KeysInput):
        return self.with_modifiers(other)

    def with_modifiers(self, modifiers: KeysInput):
        return KeyTrigger(self.trigger, self.type, self.modifiers + modifiers)

    def __repr__(self) -> str:
        modifiers = f" & {self.modifiers}" if self.modifiers else ""
        return " & ".join((self.trigger_label, repr(modifiers)))

    def __str__(self) -> str:
        return repr(self)

    @property
    def specificity(self):
        return self.trigger.specificity + self.modifiers.specificity

    def bind(self, cmd: "Act"):
        from pykeys.keys.trigger_binding import TriggerBinding

        return TriggerBinding(self, cmd)
