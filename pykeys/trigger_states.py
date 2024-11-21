from dataclasses import dataclass, field
from handler import Handler


@dataclass()
class TriggerStates:
    down: Handler | None = field(default=None)
    up: Handler | None = field(default=None)
    suppress: bool = field(default=True)

    def __str__(self):
        parts: list[str] = []
        if self.down:
            parts.append(f"↓X")
        if self.up:
            parts.append(f"↑X")
        return " ".join(parts)
