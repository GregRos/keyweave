from dataclasses import dataclass


@dataclass
class Command:
    label: str
    description: str

    def default(self, label: str | None = None, description: str | None = None):
        return Command(self.label or label or "", self.description or description or "")
