from typing import Literal


type TriggerTypeName = Literal["down", "up"]


class TriggerType:
    __match_args__ = ("name",)

    def __init__(self, name: "TriggerTypeName | TriggerType"):
        self.name = name if isinstance(name, str) else name.name

    def __hash__(self) -> int:
        return hash(self.name)

    @property
    def char(self) -> str:
        return "↓" if self.name == "down" else "↑"

    def __eq__(self, other: object) -> bool:
        match other:
            case TriggerType(other_name):
                return self.name == other_name
            case str(s):
                return self.name == s
            case _:
                return False
