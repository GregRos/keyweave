import os
import sys
from time import sleep

from pykeys import (
    key,
    LayoutClass,
    command,
    HotkeyEvent,
    HotkeyInterceptionEvent,
)

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)


class AsddBC(LayoutClass):
    a = 1

    def __intercept__(self, intercepted: HotkeyInterceptionEvent):
        print("A", self.a)
        print("Intercepted", intercepted)
        intercepted.next()

    @(key.b & key.shift + key.ctrl)
    @command(label="abc", description="ABC")
    def abc(self, e: HotkeyEvent):
        print(e)

    @(key.z & key.alt + ~key.ctrl)
    @command(label="xxx")
    def abce(self, e: HotkeyEvent):
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
