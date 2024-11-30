from dataclasses import dataclass
import time
from pykeys.key.key_trigger import KeyTrigger


class KeyEvent:
    def __init__(self, timestamp: float | None = None):
        self.timestamp = timestamp or time.time()


@dataclass(init=False)
class TriggeredKeyEvent(KeyTrigger, KeyEvent):
    def __init__(self, trigger: KeyTrigger, event: KeyEvent):
        KeyTrigger.__init__(self, trigger.trigger, trigger.type, trigger.modifiers)
        KeyEvent.__init__(self, event.timestamp)
