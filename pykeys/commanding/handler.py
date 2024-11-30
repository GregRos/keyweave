from typing import Any, Protocol

from pykeys.commanding.event import KeyEvent
from pykeys.key.key_trigger import KeyTrigger


class Handler(Protocol):
    def __call__(self, trigger: KeyTrigger, event: KeyEvent, /) -> Any: ...
