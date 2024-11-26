from pykeys.keys.key_trigger import KeyTrigger
from pykeys.handling.metadata import HotkeyMetadata


from dataclasses import dataclass, field
from time import time


@dataclass()
class HotkeyEvent(HotkeyMetadata):
    trigger: KeyTrigger
    timestamp: float = field(default_factory=lambda: time(), init=False)
