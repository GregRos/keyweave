from typing import Any, Callable, Protocol, overload
from pykeys.commanding.event import CommandEvent
from pykeys.commanding.metadata import Command
from pykeys.key.key import KeyInput
from pykeys.key.key_set import KeySet, KeysInput
from pykeys.commanding.handler import Handler
from pykeys.key.key_trigger import KeyTrigger
from pykeys.commanding.trigger_binding import CommandBinding, BindingInterceptor


type TriggerInput = "KeyTrigger | KeyInput"


class _HandlerAInst(Protocol):

    def __call__(self, other_self: Any, info: CommandEvent, /) -> Any: ...


class _HandlerBInst(Protocol):

    def __call__(self, other_self: Any, /) -> Any: ...


type InstHandler = _HandlerAInst | _HandlerBInst

type InstBindingInterceptor = Callable[[Any, CommandBinding], None]


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


def command(label: str, description: str = ""):
    def decorate[T: Handler | InstHandler](func: T) -> T:
        func.__dict__["metadata"] = Command(label, description)
        return func

    return decorate


@overload
def intercepts() -> Callable[[InstBindingInterceptor], InstBindingInterceptor]: ...


@overload
def intercepts[F: InstBindingInterceptor](f: F) -> F: ...


def intercepts[
    F: InstBindingInterceptor
](f: F | None = None) -> F | Callable[[InstBindingInterceptor], InstBindingInterceptor]:
    if f is None:

        def decorate(f: InstBindingInterceptor) -> InstBindingInterceptor:
            f.__dict__["intercepts"] = True
            return f

        return decorate
    f.__dict__["intercepts"] = True
    return f


def get_func_hotkeys(f: Callable[[], Any]) -> set[KeyTrigger]:
    return f.__dict__.get("hotkeys", set())


def is_interceptor(f: Callable[[], Any]) -> bool:
    return f.__dict__.get("intercepts", False)


def get_func_metadata(f: Callable[[], Any]) -> Command:
    return f.__dict__.get("metadata", Command("", ""))
