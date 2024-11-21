import threading
from typing import Callable

from keyboard import KeyboardEvent
from pykeys.trigger_states import TriggerStates
from pykeys.trigger_info import TriggerInfo
from pykeys.key import Key
from pykeys.key_combination import KeyCombination
from pykeys.handler import Handler


class CompoundBinding:
    __match_args__ = ("key", "cases")
    _lock = threading.Lock()

    def __init__(
        self,
        trigger: Key,
        modifiers: dict[KeyCombination, TriggerStates] = {},
    ):
        self.trigger = trigger
        self.modifiers = modifiers.copy()

    def __iter__(self):
        x = sorted(self.modifiers.items(), key=lambda x: x[0])
        return iter(x)

    def __contains__(self, key: Key | None):
        return key in self.modifiers

    def __len__(self):
        return len(self.modifiers)

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, CompoundBinding):
            return False
        return self.trigger == value.trigger and self.modifiers == value.modifiers

    def __hash__(self) -> int:
        return hash(self.trigger) ^ hash(self.modifiers)

    def whens(self, cases: dict[KeyCombination | Key, Handler]):
        cases2 = dict(
            (KeyCombination({k}) if isinstance(k, Key) else k, TriggerStates(v))
            for k, v in cases.items()
        )
        return CompoundBinding(self.trigger, {**self.modifiers, **cases2})

    def when(
        self,
        key: Key | KeyCombination,
        down: Handler | None = None,
        up: Handler | None = None,
        suppress: bool = True,
    ):
        key = KeyCombination({key}) if isinstance(key, Key) else key
        case = TriggerStates(down, up, suppress)
        return CompoundBinding(self.trigger, {**self.modifiers, key: case})

    def handler(self) -> Callable[[KeyboardEvent], bool]:
        def on_event(e: KeyboardEvent) -> bool:
            with self._lock:
                if not self.trigger.match_event(e):
                    return True
                p = max(
                    (
                        (combo, triggers)
                        for combo, triggers in self.modifiers.items()
                        if combo.is_pressed()
                    ),
                    key=lambda x: x[0],
                    default=None,
                )
                if not p:
                    return True

                combo, triggers = p
                cmd = triggers.down if e.event_type == "down" else triggers.up
                if cmd:
                    cmd(TriggerInfo(self.trigger, e.event_type, combo))
                return not triggers.suppress

        return on_event

    def default(
        self,
        down: Handler | None = None,
        up: Handler | None = None,
        suppress: bool = True,
    ):
        empty = KeyCombination(set())
        case = TriggerStates(down, up, suppress)
        return CompoundBinding(self.trigger, {**self.modifiers, empty: case})
