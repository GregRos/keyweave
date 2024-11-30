from typing import Any, Protocol

from pykeys.commanding.event import TriggeredKeyEvent


class Handler(Protocol):

    def __call__(self, event: TriggeredKeyEvent, /) -> Any: ...
