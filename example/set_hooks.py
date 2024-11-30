import os
import sys
from time import sleep

from pykeys.commanding.event import KeyEvent
from pykeys.key.key_trigger import KeyTrigger


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from pykeys.commanding.metadata import Command
from pykeys.schedulers.default import DefaultScheduler

from pykeys.layout.layout import Layout
from pykeys import key as keys
from pykeys.layout.print_layout import get_layout_table


def a(trigger: KeyTrigger, event: KeyEvent):
    print(f"It happened: {trigger}")


sch = DefaultScheduler()

lt = Layout("messing_with_keys", sch)
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
