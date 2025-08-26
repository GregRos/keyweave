from dataclasses import dataclass, field
import inspect
from typing import TYPE_CHECKING, Any

from pykeys.commanding.handler import FuncHotkeyHandler, HotkeyHandler

if TYPE_CHECKING:
    from pykeys.commanding.event import HotkeyEvent
    from pykeys.key.hotkey import Hotkey


@dataclass(kw_only=True)
class CommandInfo:
    label: str | None
    description: str | None = field(default=None, kw_only=True)
    emoji: str | None = field(default=None, kw_only=True)


@dataclass
class Command:
    info: CommandInfo
    handler: FuncHotkeyHandler

    def bind(self, hotkey: "Hotkey"):
        from ..bindings.binding import Binding

        return Binding(hotkey.info, self)


class CommandProducer:
    def __init__(self, func: HotkeyHandler, cmd: CommandInfo):
        self.func = func
        self.cmd = cmd

    def _make(self, instance: object | None = None):
        def wrapper(event: "HotkeyEvent", /) -> Any:
            arg_count = len(inspect.signature(self.func).parameters)
            match arg_count:
                case 1:
                    return self.func(event)  # type: ignore
                case 2:
                    return self.func.__get__(instance)(event)  # type: ignore
                case _:
                    raise ValueError("Invalid number of arguments")

        return Command(
            info=self.cmd,
            handler=wrapper,
        )

    def __get__(
        self, instance: object | None, owner: type | None = None
    ) -> Command:
        return self._make(instance)


type CommandOrProducer = Command | CommandProducer


@dataclass
class command(CommandInfo):

    def __call__(self, handler: HotkeyHandler) -> "CommandProducer":
        return CommandProducer(handler, cmd=self)


def resolve_command(
    cmd: CommandOrProducer, instance: object | None = None
) -> Command:
    if isinstance(cmd, CommandProducer):
        return cmd.__get__(instance, type(instance) if instance else None)
    return cmd
