from concurrent.futures import thread
import os
import sys
from time import sleep


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from pykeys.schedulers.thread_pool import ThreadPoolScheduler

from pykeys.keys.cmd import Act, EventInfo
from pykeys.layout.layout import Layout
from pykeys.keys import keys
from pykeys.layout.print_layout import get_layout_table


def a(event: EventInfo):
    print(f"It happened: {event.label}")


sch = ThreadPoolScheduler()

lt = Layout("messing_with_keys", sch)
lt += keys.num_1.down.with_modifiers(keys.num_0).bind(
    label="a", handler=a, description="something something"
)
lt += keys.num_1.down.with_modifiers(keys.num_dot).bind(
    label="a", handler=a, description="something something"
)
lt += keys.num_1.down.bind(label="a", handler=a, description="something something")
lt += keys.num_2.down.bind(label="a", handler=a, description="something something")

lt.__enter__()
sleep(1000)
print(get_layout_table(lt))
