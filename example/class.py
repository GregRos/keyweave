import os
import sys
from time import sleep


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from pykeys.handling.event import HotkeyEvent

from pykeys.keys import keys
from pykeys.layout_class.decorators import hotkey
from pykeys.layout_class.layout_class import hotkey_layout


@hotkey_layout(name="my super special awesome layout")
class AsddBC:

    @hotkey(keys.num_1)
    def abc(self, event: HotkeyEvent):
        print(event)

    @hotkey(keys.num_1.down.with_modifiers(keys.num_0))
    def abcd(self, event: HotkeyEvent):
        print(event)

    @hotkey(keys.num_3, modifiers=keys.num_dot + keys.num_0)
    def abcde(self, event: HotkeyEvent):
        print(event)


AsddBC.__enter__()
sleep(1000)
