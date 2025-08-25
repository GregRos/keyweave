import os
import sys
from time import sleep

from pykeys import key
from pykeys.bindings.interceptor import HotkeyInterceptionEvent
from pykeys.commanding.decorator import command

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)


from pykeys.commanding.event import HotkeyEvent


from pykeys.layout_class.layout_class import LayoutClass


class AsddBC(LayoutClass):

    def __intercept__(self, intercepted: HotkeyInterceptionEvent):
        print("Intercepted", intercepted)

    @(key.b & key.shift + key.ctrl)
    @command("abc", "ABC")
    def abc(self, e: HotkeyEvent):
        print(e)

    @(key.a & key.shift + key.ctrl)
    @command("abc", "ABC")
    def abcd(self, e: HotkeyEvent):
        print(e)

    @(key.c & key.shift + key.ctrl)
    @command("abc", "ABC")
    def abcde(self, e: HotkeyEvent):
        print(e)


lt = AsddBC()

with lt:
    sleep(1000)
