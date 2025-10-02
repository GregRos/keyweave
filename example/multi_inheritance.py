import os
import sys
from time import sleep
import log_setup
from keyweave import (
    key,
    LayoutClass,
    command,
    HotkeyEvent,
    HotkeyInterceptionEvent,
)

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)


class Base_0(LayoutClass):

    @(key.c & [key.shift, key.ctrl])
    @command(label="abc", description="ABC")
    def abcde(self, e: HotkeyEvent):
        print(e)


class Base_1(Base_0, LayoutClass):
    a = 1

    def __intercept__(self, intercepted: HotkeyInterceptionEvent):
        print("A", self.a)
        print("Intercepted", intercepted)
        intercepted.next()

    @(key.b.down & [key.shift, key.ctrl])
    @command(label="abc", description="ABC")
    def abc(self, e: HotkeyEvent):
        print(e)

    @(key.z.down & [key.alt, ~key.ctrl] + [key.alt])
    @command(label="xxx")
    def abce(self, e: HotkeyEvent):
        print(e)


class Base_2(LayoutClass):

    @(key.a & [key.shift, key.ctrl])
    @command(label="abc", description="ABC")
    def abcd(self, e: HotkeyEvent):
        print(e)


class Inherited(Base_1, Base_2, LayoutClass):
    pass


lt = Inherited()

with lt:
    sleep(1000)
