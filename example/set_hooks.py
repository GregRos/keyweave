import os
import sys
from time import sleep

from pykeys.commanding.event import HotkeyEvent
from pykeys.schedulers.default import default_scheduler


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from pykeys.commanding.command import Command

from pykeys.layout.layout import Layout
from pykeys import key as keys
from pykeys.layout.print_layout import get_layout_table


def on_error(e: BaseException):
    print(f"Error: {e}")


def a(e: HotkeyEvent):
    print(f"It happened: {e}")


scheduler = default_scheduler(on_error)

lt = Layout("messing_with_keys", scheduler)
lt += keys.num_1.down.bind(handler=a, metadata=Command("a", "something something"))
lt += keys.num_1.down.with_modifiers(keys.num_0).bind(
    handler=a, metadata=Command("a", "something something")
)
lt += keys.num_1.down.with_modifiers(keys.num_dot).bind(
    handler=a, metadata=Command("a", "something something")
)
lt += keys.num_1.down.bind(handler=a, metadata=Command("a", "something something"))
lt.__enter__()
sleep(1000)
print(get_layout_table(lt))
