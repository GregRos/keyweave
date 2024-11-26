from typing import Any, Callable, Protocol
from pykeys.keys.event import HotkeyEvent
from pykeys.keys.metadata import HotkeyMetadata
from pykeys.keys.key import KeyInput
from pykeys.keys.key_set import KeySet, KeysInput
from pykeys.keys.handler import Handler
from pykeys.keys.key_trigger import KeyTrigger


type TriggerInput = "KeyTrigger | KeyInput"


class _HandlerAInst(Protocol):

    def __call__(self, other_self: Any, info: HotkeyEvent, /) -> Any: ...


class _HandlerBInst(Protocol):

    def __call__(self, other_self: Any, /) -> Any: ...


type InstHandler = _HandlerAInst | _HandlerBInst


def hotkey(trigger: TriggerInput, modifiers: KeysInput = KeySet()):
    combined_trigger = (
        trigger if isinstance(trigger, KeyTrigger) else KeyTrigger(trigger, "down")
    )
    combined_trigger = combined_trigger.with_modifiers(modifiers)

    def decorate[T: Handler | InstHandler](func: T) -> T:
        hotkeys: set[KeyTrigger] = func.__dict__.setdefault("hotkeys", set())
        hotkeys.add(combined_trigger)

        return func

    return decorate


def metadata(label: str, description: str = ""):
    def decorate[T: Handler | InstHandler](func: T) -> T:
        func.__dict__["metadata"] = HotkeyMetadata(label, description)
        return func

    return decorate


def get_func_hotkeys(f: Callable[[], Any]) -> set[KeyTrigger]:
    return f.__dict__.get("hotkeys", set())


def get_func_metadata(f: Callable[[], Any]) -> HotkeyMetadata:
    return f.__dict__.get("metadata", HotkeyMetadata("", ""))
