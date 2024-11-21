from dataclasses import dataclass
from pykeys.key import Key
from pykeys.key_combination import KeyCombination


@dataclass(init=False, eq=True)
class TriggerCombination:
    trigger: Key
    modifiers: KeyCombination

    def __init__(self, trigger: Key, modifiers: KeyCombination | Key):
        self.trigger = trigger
        self.modifiers = KeyCombination(modifiers)

    def __str__(self):
        return f"{self.trigger} → {self.modifiers}"
