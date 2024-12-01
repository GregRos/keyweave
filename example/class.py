import os
import sys
from time import sleep

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pykeys.commanding.event import InputEvent, HotkeyEvent
from pykeys.key.key_trigger import Hotkey
from pykeys.bindings.interception import InterceptedAction


from pykeys import key as keys
from pykeys.layout_class.decorators import hotkey, intercepts
from pykeys.layout_class.layout_class import layout


@layout(name="my super special awesome layout")
class AsddBC:

    @intercepts()
    def intercept(self, action: InterceptedAction):
        print(f"Intercepted {action}")

    @hotkey(keys.num_1)
    def abc(self, e: HotkeyEvent):
        print(e)

    @hotkey(keys.num_1.down.with_modifiers(keys.num_0))
    def abcd(self, e: HotkeyEvent):
        print(e)

    @hotkey(keys.num_3, modifiers=keys.num_dot + keys.num_0)
    def abcde(self, e: HotkeyEvent):
        print(e)


AsddBC.__enter__()
sleep(1000)
