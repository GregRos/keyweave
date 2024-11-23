from typing import Literal


type TriggerTypeName = Literal["down", "up"]


class TriggerType:
    def __init__(self, name: TriggerTypeName):
        self.name = name

    @property
    def char(self) -> str:
        return "↓" if self.name == "down" else "↑"
