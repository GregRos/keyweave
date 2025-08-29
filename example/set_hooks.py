from time import sleep
from keyweave import key, command, HotkeyEvent, Layout


def on_error(e: BaseException):
    print(f"Error: {e}")


@command(label="xyz", description="abc")
def xyz(e: HotkeyEvent):
    print(f"It happened: {e}")


@command(label="xyz", description="abc")
def abc(e: HotkeyEvent):
    print(f"abc: {e}")


lt = Layout.create(
    "my_layout", {key.a & [key.alt, key.ctrl]: xyz, key.num_2: abc}
)
with lt:
    sleep(1000)
