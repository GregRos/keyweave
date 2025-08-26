from dataclasses import dataclass
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pykeys.commanding.command import Command
    from pykeys.key.hotkey import HotkeyInfo


class InputEvent:
    def __init__(self, timestamp: float | None = None):
        self.timestamp = timestamp or time.time()


@dataclass
class HotkeyEvent:
    hotkey: "HotkeyInfo"
    event: InputEvent
    command: "Command"
