from typing import Any
from pykeys.commanding.decorator import CommandDecorator, resolve_command
from pykeys.key.hotkey import Hotkey
from pykeys.bindings.binding import Binding
from pykeys.commanding.command import Command


def hotkey(hotkey: Hotkey):
    class HotkeyDecorator:
        def __init__(self, cmd: Command | CommandDecorator[Any]):
            self.cmd = cmd

        def __get__(self, instance: Any, owner: type) -> Binding:
            cmd = resolve_command(self.cmd, instance)
            return Binding(hotkey.info, cmd)

    return HotkeyDecorator
