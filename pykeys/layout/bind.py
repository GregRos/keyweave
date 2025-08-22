from pykeys.key.hotkey import Hotkey
from pykeys.bindings.binding import Binding
from pykeys.commanding.command import Command


def hotkey(hotkey: Hotkey):

    def decorator(cmd: Command) -> Binding:
        return Binding(hotkey, cmd)

    return decorator
