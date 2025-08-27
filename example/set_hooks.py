from time import sleep
from pykeys import key
from pykeys._commanding import command, HotkeyEvent
from pykeys._layout.layout import Layout
from pykeys.scheduling import default_scheduler


def on_error(e: BaseException):
    print(f"Error: {e}")


@command(label="xyz", description="abc")
def xyz(e: HotkeyEvent):
    print(f"It happened: {e}")


@command(label="xyz", description="abc")
def abc(e: HotkeyEvent):
    print(f"abc: {e}")


scheduler = default_scheduler(on_error)
lt = Layout.create(
    "my_layout", {key.a & key.alt + key.ctrl: xyz, key.num_2: abc}
)
with lt:
    sleep(1000)
