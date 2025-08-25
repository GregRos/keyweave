from time import sleep
from pykeys import key
from pykeys.commanding.decorator import commandx
from pykeys.commanding.event import HotkeyEvent
from pykeys.layout.layout import Layout
from pykeys.schedulers.default import default_scheduler


def on_error(e: BaseException):
    print(f"Error: {e}")


@commandx(label="xyz", description="abc")
def xyz(e: HotkeyEvent):
    print(f"It happened: {e}")


@commandx(label="xyz", description="abc")
def abc(e: HotkeyEvent):
    print(f"abc: {e}")


scheduler = default_scheduler(on_error)
lt = Layout.create(
    "my_layout", {key.a & key.alt + key.ctrl: xyz, key.num_2: abc}
)
with lt:
    sleep(1000)
