from dataclasses import dataclass
import time
from pykeys.commanding.command import Command
from pykeys.key.hotkey import Hotkey


class InputEvent:
    def __init__(self, timestamp: float | None = None):
        self.timestamp = timestamp or time.time()


@dataclass
class HotkeyEvent:
    hotkey: Hotkey
    event: InputEvent
    command: Command
