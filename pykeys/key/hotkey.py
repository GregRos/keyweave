from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from pykeys.key.key import Key, KeyInput
from pykeys.key.key_set import KeySet, KeysInput
from pykeys.key.key_event_type import KeyEventType, TriggerTypeName

if TYPE_CHECKING:
    from pykeys.commanding.command import Command
    from pykeys.commanding.decorator import CommandDecorator
    from pykeys.bindings.binding import Binding


@dataclass(order=True, eq=True, frozen=True, unsafe_hash=True)
class HotkeyInfo:
    __match_args__ = ("key", "type", "modifiers")
    trigger: Key
    type: KeyEventType
    modifiers: KeySet = field(default=KeySet())
    passthrough: bool = field(default=False, compare=False)

    @property
    def specificity(self) -> int:
        return self.trigger.specificity + self.modifiers.specificity

    @property
    def trigger_label(self) -> str:
        return f"{self.type.char} {self.trigger}"

    def __repr__(self) -> str:
        if not self.modifiers:
            return f"{self.trigger_label}"
        else:
            return f"{self.trigger_label} & {self.modifiers}"

    def __str__(self) -> str:
        return repr(self)


@dataclass(order=True, eq=True, frozen=True, unsafe_hash=True)
class Hotkey:
    info: HotkeyInfo

    def passthrough(self, enable: bool = True):
        return Hotkey(
            HotkeyInfo(
                trigger=self.info.trigger,
                type=self.info.type,
                modifiers=self.info.modifiers,
                passthrough=enable,
            )
        )

    @property
    def is_down(self) -> bool:
        return self.info.type == "down"

    def __call__(self, handler: "Command | CommandDecorator[Any]"):
        from pykeys.commanding.decorator import resolve_command

        hk = self

        class BindInstance:
            def __get__(self, instance: object, owner: type) -> "Binding":
                return resolve_command(handler, instance).bind(hk)

        return BindInstance()

    @property
    def is_up(self) -> bool:
        return self.info.type == "up"

    def __and__(self, other: KeysInput):
        return self.modifiers(other)

    def modifiers(self, modifiers: KeysInput):
        return Hotkey(
            HotkeyInfo(
                trigger=self.info.trigger,
                type=self.info.type,
                modifiers=self.info.modifiers + modifiers,
                passthrough=self.info.passthrough,
            )
        )


type HotkeyInput = Hotkey | HotkeyInfo


def resolve_hotkey(input: HotkeyInput, /) -> HotkeyInfo:
    match input:
        case HotkeyInfo():
            return input
        case Hotkey():
            return input.info
