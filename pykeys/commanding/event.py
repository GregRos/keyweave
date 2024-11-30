from dataclasses import dataclass, field
from time import time


@dataclass
class KeyEvent:
    timestamp: float = field(default_factory=lambda: time(), init=False)
