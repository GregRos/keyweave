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
            if inspect.ismethod(self.func):
                return self.func.__get__(instance)(event)
            return self.func(event)  # type: ignore

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


def commandx[T](label: str | None = None, description: str | None = None):

    def deco(func: HotkeyHandler):
        return CommandDecorator[T](
            func, cmd=AbsCommand(label=label, description=description)
        )

    return deco
