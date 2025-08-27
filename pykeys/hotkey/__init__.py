from dataclasses import dataclass, field
import time
from typing import TYPE_CHECKING

from pykeys.commanding import CommandProducer, resolve_command
from pykeys.key_types import Key, KeySet, KeysInput, KeyEventType

if TYPE_CHECKING:
    from pykeys.commanding import Command
    from pykeys.bindings import Binding


@dataclass(order=True, eq=True, frozen=True, unsafe_hash=True)
class HotkeyInfo:
    __match_args__ = ("key", "type", "modifiers", "passthrough")
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

    def __call__(self, cmd: "Command | CommandProducer"):
        from ..bindings import BindingProducer

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


@dataclass
class InputEvent:
    timestamp: float | None = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()


@dataclass
class HotkeyEvent:
    hotkey: "HotkeyInfo"
    event: InputEvent
    command: "Command"
