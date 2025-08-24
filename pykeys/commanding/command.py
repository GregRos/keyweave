from dataclasses import dataclass, field

from pykeys.commanding.handler import FuncHotkeyHandler


@dataclass
class AbsCommand:
    label: str | None
    description: str | None = field(default=None, kw_only=True)
    emoji: str | None = field(default=None, kw_only=True)


@dataclass
class UnboundCommand(AbsCommand):

    def handle(self, handler: FuncHotkeyHandler):
        Command(label=self.label, description=self.description, handler=handler)


@dataclass
class Command(AbsCommand):
    handler: FuncHotkeyHandler
