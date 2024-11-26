from dataclasses import dataclass


@dataclass
class HotkeyMetadata:
    label: str
    description: str

    def default(self, label: str | None = None, description: str | None = None):
        return HotkeyMetadata(
            self.label or label or "", self.description or description or ""
        )
