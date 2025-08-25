import inspect
from typing import Any

from pykeys.commanding.command import AbsCommand, Command
from pykeys.commanding.handler import HotkeyHandler
from pykeys.commanding.event import HotkeyEvent


class CommandDecorator[T]:
    def __init__(self, func: HotkeyHandler, cmd: AbsCommand):
        self.func = func
        self.cmd = cmd

    def _make(self, instance: T | None = None):
        def wrapper(event: HotkeyEvent, /) -> Any:
            arg_count = len(inspect.signature(self.func).parameters)
            match arg_count:
                case 1:
                    return self.func(event)  # type: ignore
                case 2:
                    return self.func.__get__(instance)(event)  # type: ignore
                case _:
                    raise ValueError("Invalid number of arguments")

        return Command(
            label=self.cmd.label or self.func.__qualname__,
            description=self.cmd.description,
            handler=wrapper,
        )

    def __get__(
        self, instance: T | None, owner: type[T] | None = None
    ) -> Command:
        return self._make(instance)


type CommandOrDecorator = Command | CommandDecorator[Any]


def resolve_command(
    cmd: CommandOrDecorator, instance: object | None = None
) -> Command:
    if isinstance(cmd, CommandDecorator):
        return cmd.__get__(instance, type(instance) if instance else None)
    return cmd


def command[T](label: str | None = None, description: str | None = None):

    def deco(func: HotkeyHandler):
        return CommandDecorator[T](
            func, cmd=AbsCommand(label=label, description=description)
        )

    return deco
