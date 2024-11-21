from dataclasses import dataclass
import time
from typing import Literal

from pykeys.key import Key
from pykeys.key_combination import KeyCombination


@dataclass()
class TriggerInfo:
    trigger: Key
    event: Literal["down", "up", None]
    modifiers: KeyCombination

    def __post_init__(self):
        self.timestamp = time.time()

    def __str__(self):
        # up arrow or down arrow
        up_down = "↑" if self.event == "up" else "↓"
        return f"{up_down}{self.trigger} & {self.modifiers}"
