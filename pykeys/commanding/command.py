from dataclasses import dataclass

from pykeys.commanding.handler import HotkeyHandler


@dataclass
class AbsCommand:
    label: str
    description: str

    def default(self, label: str | None = None, description: str | None = None):
        return AbsCommand(
            self.label or label or "", self.description or description or ""
        )

    def handle(self, handler: HotkeyHandler):
        Command(self.label, self.label, handler)


@dataclass
class Command:
    label: str
    description: str
    handler: HotkeyHandler
