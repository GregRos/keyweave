import os
import sys
from time import sleep

from pykeys import key
from pykeys.commanding.decorator import commandx
from pykeys.layout.bind import hotkey

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)


from pykeys.commanding.event import HotkeyEvent


from pykeys.layout_class.layout_class import LayoutClass


class AsddBC(LayoutClass):

    @hotkey(key.a & key.shift + key.ctrl)
    @commandx("abc", "ABC")
    def abc(self, e: HotkeyEvent):
        print(e)

    @commandx("abc", "ABC")
    def abcd(self, e: HotkeyEvent):
        print(e)

    @commandx("abc", "ABC")
    def abcde(self, e: HotkeyEvent):
        print(e)


lt = AsddBC()

with lt:
    sleep(1000)
