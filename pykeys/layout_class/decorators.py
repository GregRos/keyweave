from typing import Any, Protocol
from pykeys.key_types import KeyInput

from pykeys.hotkey import Hotkey, HotkeyEvent
from pykeys.bindings import HotkeyInterceptionEvent


type TriggerInput = "Hotkey | KeyInput"


class InstHandler(Protocol):

    def __call__(self, other_self: Any, event: HotkeyEvent, /) -> Any: ...


class InstActionInterceptor(Protocol):

    def __call__(
        self, other_self: Any, action: HotkeyInterceptionEvent, /
    ) -> Any: ...


def intercepts():

    def decorate(
        func: InstActionInterceptor,
    ) -> InstActionInterceptor:
        func.__dict__["intercepts"] = True
        return func

    return decorate
