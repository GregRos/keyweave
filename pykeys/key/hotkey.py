from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from pykeys.commanding import CommandProducer, resolve_command
from pykeys.key.key import Key
from pykeys.key.key_set import KeySet, KeysInput
from pykeys.key.key_event_type import KeyEventType

if TYPE_CHECKING:
    from pykeys.commanding import Command
    from pykeys.bindings.bindings import Binding


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


@dataclass
class BindingProducer:
    cmd: "Command | CommandProducer"
    hotkey: "Hotkey"

    def __get__(self, instance: object, owner: type) -> "Binding":
        r_cmd = resolve_command(self.cmd, instance)

        return r_cmd.bind(self.hotkey)


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

    def __call__(self, cmd: "Command | CommandProducer"):

        return BindingProducer(cmd, self)

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


def hotkey(hotkey: Hotkey):
    return hotkey
