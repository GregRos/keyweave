import os
import sys
from time import sleep as sync_sleep
import log_setup
from keyweave import (
    key,
    LayoutClass,
    command,
    HotkeyEvent,
    HotkeyInterceptionEvent,
)
from asyncio import sleep

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)


class AsddBC(LayoutClass):
    a = 1

    async def __intercept__(self, intercepted: HotkeyInterceptionEvent):
        print("A", self.a)
        print("Intercepted", intercepted)
        await intercepted.next()
        print("Awaited!")

    def also_interceptor(self, intercepted: HotkeyInterceptionEvent):
        print("Also intercepted", intercepted)
        intercepted.end()
        print("Ended!")

    @key.y.down[key.shift, key.ctrl]
    @command(interceptor=also_interceptor)
    async def affb(self, e: HotkeyEvent):
        await sleep(0.3)
        print(e)

    @key.p.down[key.shift, key.ctrl]
    @command(interceptor=False)
    async def abxx(self, e: HotkeyEvent):
        await sleep(0.3)
        print(e)

    @key.a.down[key.shift, key.ctrl]
    @command(interceptor=True)
    async def ab(self, e: HotkeyEvent):
        await sleep(0.3)
        print(e)

    @key.b.down[key.shift, key.ctrl]
    @command(label="abc", description="ABC")
    async def abc(self, e: HotkeyEvent):
        await sleep(0.3)
        print(e)

    @key.z.down[key.alt, ~key.ctrl, key.alt]
    @command(label="xxx")
    async def abce(self, e: HotkeyEvent):
        await sleep(0.3)
        print(e)

    @key.a[key.shift, key.ctrl]
    @command(
        label="abc",
        description="ABC long description here to test wrapping and stuff",
    )
    async def abcd(self, e: HotkeyEvent):
        await sleep(0.3)
        print(e)

    @(key.c & [key.shift, key.ctrl])
    @command(label="abc", description="ABC")
    async def abcde(self, e: HotkeyEvent):
        await sleep(0.3)
        print(e)

    @(key.h & [key.shift, key.ctrl])
    @command(label="abc", description="ABC")
    def abcde2(self, e: HotkeyEvent):
        sync_sleep(0.3)
        print(e)


lt = AsddBC()

with lt:
    sync_sleep(1000)
