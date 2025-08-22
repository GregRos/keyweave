from typing import Any, Protocol
from pykeys.commanding.event import HotkeyEvent
from pykeys.key.key import KeyInput

from pykeys.key.hotkey import Hotkey
from pykeys.bindings.interceptor import InterceptedHotkey


type TriggerInput = "Hotkey | KeyInput"


class InstHandler(Protocol):

    def __call__(self, other_self: Any, event: HotkeyEvent, /) -> Any: ...


class InstActionInterceptor(Protocol):

    def __call__(self, other_self: Any, action: InterceptedHotkey, /) -> Any: ...


def intercepts():

    def decorate(
        func: InstActionInterceptor,
    ) -> InstActionInterceptor:
        func.__dict__["intercepts"] = True
        return func

    return decorate
