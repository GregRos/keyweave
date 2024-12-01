import threading
from typing import Any
from pykeys.bindings.key_binding_collection import KeyBindingCollection
from pykeys.commanding.event import InputEvent
from pykeys.key.key import Key

from pykeys.key.key_set import KeySet
from keyboard import KeyboardEvent, hook_key, is_pressed, unhook

from win32api import GetAsyncKeyState  # type: ignore


from typing import Any

from pykeys.schedulers.scheduling import Scheduler


class KeyHook:
    _internal_handler: Any
    _lock = threading.Lock()

    def __init__(
        self, key: Key, collection: KeyBindingCollection, scheduler: Scheduler
    ):
        self.key = key
        self._collection = collection
        self._scheduler = scheduler
        self.manufactured_handler = self._get_handler()

    def __enter__(self):
        self._internal_handler = hook_key(
            _get_keyboard_hook_id(self.key), self.manufactured_handler, suppress=True
        )
        return self

    def __exit__(self):
        unhook(self._internal_handler)
        return self

    def _get_handler(self):
        def get_best_binding(event: KeyboardEvent):
            only_matching = [
                binding
                for binding in self._collection
                if binding.hotkey.trigger.is_numpad == event.is_keypad
                and _is_key_set_active(binding.hotkey.modifiers)
                and binding.hotkey.type == event.event_type
            ]

            by_specificity = sorted(
                only_matching,
                key=lambda binding: binding.hotkey.specificity,
                reverse=True,
            )
            return by_specificity[0] if by_specificity else None

        def handler(info: KeyboardEvent):
            binding = get_best_binding(info)
            if not binding:
                return True

            def binding_invoker():
                binding(InputEvent(info.time))

            self._scheduler(binding_invoker)
            return False

        return handler


def _get_keyboard_hook_id(key: Key) -> str:
    match key.id:
        case "num:enter":
            return "enter"
        case "num:dot" | "num:.":
            return "."
        case "num:star" | "num:*" | "num:multiply":
            return "*"
        case "num:plus" | "num:+":
            return "+"
        case "num:minus" | "num:-":
            return "-"
        case "num:slash" | "num:/":
            return "/"
        case "mouse:1":
            return "left"
        case "mouse:2":
            return "right"
        case "mouse:3":
            return "middlemouse"
        case "mouse:4":
            return "x"
        case "mouse:5":
            return "x2"
        case _:
            return key.id.replace("num:", "num ")


def _get_windows_id_for_mouse_key(key: Key) -> int:
    if key.is_mouse:
        return int(key.id.replace("mouse:", ""))
    raise ValueError("Key is not a mouse key")


def _is_pressed(key: Key):
    if key.is_mouse:
        id = _get_windows_id_for_mouse_key(key)
        pr: Any = GetAsyncKeyState(id) & 0x8000
        return pr
    else:
        hook_id = _get_keyboard_hook_id(key)
        return is_pressed(hook_id)


def _is_key_set_active(key_set: KeySet):
    return all(_is_pressed(key) for key in key_set)
