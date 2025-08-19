from functools import wraps
from typing import Callable

from pykeys.commanding.command import Command
from pykeys.commanding.handler import HotkeyHandler
from pykeys.commanding.event import HotkeyEvent


def command(label: str, description: str) -> Callable[[HotkeyHandler], Command]:
    """Decorator to create a Command from a function that handles a HotkeyEvent.

    Usage:
            @command("my.label", "does something")
            def handler(e: HotkeyEvent):
                    ...

    The decorated function must accept a single positional argument of type
    HotkeyEvent. The decorator returns an ExecCommand whose handler wraps the
    original function.
    """

    def decorator(func: HotkeyHandler) -> Command:
        @wraps(func)
        def wrapper(event: HotkeyEvent, /):
            return func(event)

        return Command(label, description, wrapper)

    return decorator
