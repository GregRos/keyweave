from pykeys.key import Key
from pykeys.key_combination import KeyCombination


class TriggerCombination:
    trigger: Key
    modifiers: KeyCombination
    up: bool = False

    def __init__(self, trigger: Key, modifiers: KeyCombination | Key, up: bool = False):
        self.trigger = trigger
        self.modifiers = KeyCombination(modifiers)
        self.up = up

    def __str__(self):
        return f"{self.trigger} → {self.modifiers}"

    @property
    def up(self):
        return TriggerCombination(self.trigger, self.modifiers, up=True)

    @property
    def down(self):
        return TriggerCombination(self.trigger, self.modifiers, up=False)
