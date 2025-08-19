import os
import sys
from time import sleep

from pykeys.commanding.decorator import command
from pykeys.commanding.command import AbsCommand, Command
from pykeys.commanding.event import HotkeyEvent
from pykeys.layout.layout import Layout
from pykeys.schedulers.default import default_scheduler


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pykeys.layout.print_layout import get_layout_table


def on_error(e: BaseException):
    print(f"Error: {e}")


@command(label="xyz", description="abc")
def a(e: HotkeyEvent):
    print(f"It happened: {e}")


scheduler = default_scheduler(on_error)
lt = Layout.create(
    "my_layout", {keys.num_1: AbsCommand("hello", "does stuff").handle()}
)

sleep(1000)
