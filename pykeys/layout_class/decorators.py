from typing import Any, Callable, Protocol
from pykeys.commanding.event import HotkeyEvent
from pykeys.commanding.command import Command
from pykeys.key.key import KeyInput
from pykeys.key.key_set import KeySet, KeysInput
from pykeys.commanding.handler import Handler
from pykeys.key.hotkey import Hotkey
from pykeys.bindings.interceptor import InterceptedAction


type TriggerInput = "Hotkey | KeyInput"


class InstHandler(Protocol):

    def __call__(self, other_self: Any, event: HotkeyEvent, /) -> Any: ...


def hotkey(trigger: TriggerInput, modifiers: KeysInput = KeySet()):
    combined_hotkey = (
        trigger if isinstance(trigger, Hotkey) else Hotkey(trigger, "down")
    )
    combined_hotkey = combined_hotkey.with_modifiers(modifiers)

    def decorate(func: InstHandler) -> Handler | InstHandler:
        hotkeys: set[Hotkey] = func.__dict__.setdefault("hotkeys", set())
        hotkeys.add(combined_hotkey)

        return func

    return decorate


def command(label: str, description: str = ""):
    def decorate[T: Handler | InstHandler](func: T) -> T:
        func.__dict__["metadata"] = Command(label, description)
        return func

    return decorate


class InstActionInterceptor(Protocol):

    def __call__(self, other_self: Any, action: InterceptedAction, /) -> Any: ...


def intercepts():

    def decorate(
        func: InstActionInterceptor,
    ) -> InstActionInterceptor:
        func.__dict__["intercepts"] = True
        return func

    return decorate


def get_func_hotkeys(f: Callable[[], Any]) -> set[Hotkey]:
    return f.__dict__.get("hotkeys", set())


def is_interceptor(f: Callable[[], Any]) -> bool:
    return f.__dict__.get("intercepts", False)


def get_func_metadata(f: Callable[[], Any]) -> Command:
    return f.__dict__.get("metadata", Command("", ""))
