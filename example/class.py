import os
import sys
from time import sleep

from pykeys import (
    key,
    LayoutClass,
)
from pykeys.commanding import command
from pykeys.hotkey import HotkeyEvent
from pykeys.interception import HotkeyInterceptionEvent
from pykeys.layout import LayoutClass

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)


class AsddBC(LayoutClass):

    def __intercept__(self, intercepted: HotkeyInterceptionEvent):
        print("Intercepted", intercepted)

    @(key.b & key.shift + key.ctrl)
    @command(label="abc", description="ABC")
    def abc(self, e: HotkeyEvent):
        print(e)

    @(key.a & key.shift + key.ctrl)
    @command(label="abc", description="ABC")
    def abcd(self, e: HotkeyEvent):
        print(e)

    @(key.c & key.shift + key.ctrl)
    @command(label="abc", description="ABC")
    def abcde(self, e: HotkeyEvent):
        print(e)


lt = AsddBC()

with lt:
    sleep(1000)
