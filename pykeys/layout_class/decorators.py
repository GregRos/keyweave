from typing import Any, Callable, Protocol
from pykeys.commanding.event import KeyEvent
from pykeys.commanding.metadata import Command
from pykeys.key.key import KeyInput
from pykeys.key.key_set import KeySet, KeysInput
from pykeys.commanding.handler import Handler
from pykeys.key.key_trigger import KeyTrigger
from pykeys.layout.interception import InterceptedAction


type TriggerInput = "KeyTrigger | KeyInput"


class InstHandler(Protocol):

    def __call__(
        self, other_self: Any, trigger: KeyTrigger, event: KeyEvent, /
    ) -> Any: ...


def hotkey(trigger: TriggerInput, modifiers: KeysInput = KeySet()):
    combined_trigger = (
        trigger if isinstance(trigger, KeyTrigger) else KeyTrigger(trigger, "down")
    )
    combined_trigger = combined_trigger.with_modifiers(modifiers)

    def decorate(func: InstHandler) -> Handler | InstHandler:
        hotkeys: set[KeyTrigger] = func.__dict__.setdefault("hotkeys", set())
        hotkeys.add(combined_trigger)

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


def get_func_hotkeys(f: Callable[[], Any]) -> set[KeyTrigger]:
    return f.__dict__.get("hotkeys", set())


def is_interceptor(f: Callable[[], Any]) -> bool:
    return f.__dict__.get("intercepts", False)


def get_func_metadata(f: Callable[[], Any]) -> Command:
    return f.__dict__.get("metadata", Command("", ""))
