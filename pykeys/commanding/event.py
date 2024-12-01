from dataclasses import dataclass
import time
from pykeys.key.key_trigger import Hotkey


class InputEvent:
    def __init__(self, timestamp: float | None = None):
        self.timestamp = timestamp or time.time()


@dataclass(init=False)
class HotkeyEvent(Hotkey, InputEvent):
    def __init__(self, trigger: Hotkey, event: InputEvent):
        Hotkey.__init__(self, trigger.trigger, trigger.type, trigger.modifiers)
        InputEvent.__init__(self, event.timestamp)
