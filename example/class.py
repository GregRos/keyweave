import os
import sys
from time import sleep

from pykeys.commanding.trigger_binding import CommandBinding


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from pykeys.commanding.event import CommandEvent

from pykeys import key as keys
from pykeys.layout_class.decorators import hotkey, intercepts
from pykeys.layout_class.layout_class import layout


@layout(name="my super special awesome layout")
class AsddBC:

    @intercepts
    def intercept(self, binding: CommandBinding):
        print(f"Intercepted {binding}")

    @hotkey(keys.num_1)
    def abc(self, event: CommandEvent):
        print(event)

    @hotkey(keys.num_1.down.with_modifiers(keys.num_0))
    def abcd(self, event: CommandEvent):
        print(event)

    @hotkey(keys.num_3, modifiers=keys.num_dot + keys.num_0)
    def abcde(self, event: CommandEvent):
        print(event)


AsddBC.__enter__()
sleep(1000)
