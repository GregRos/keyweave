from typing import Any
from pykeys.bindings.key_binding_collection import KeyBindingCollection
from pykeys.keys.key import Key

from pykeys.keys.key_set import KeySet
from pykeys.layout.keyboard_processing import create_handler  # type: ignore
from keyboard import KeyboardEvent, hook_key, is_pressed, unhook

from win32api import GetAsyncKeyState  # type: ignore


from typing import Any


class KeyHook:
    _internal_handler: Any

    def _get_handler(self):
        def get_best_binding(event: KeyboardEvent):
            only_matching = [
                binding
                for binding in self._collection
                if binding.trigger.trigger.is_numpad == event.is_keypad
                and _is_key_set_active(binding.trigger.modifiers)
                and binding.trigger.type == event.event_type
            ]

            by_specificity = sorted(
                only_matching,
                key=lambda binding: binding.trigger.specificity,
                reverse=True,
            )
            return by_specificity[0] if by_specificity else None

        def handler(event: KeyboardEvent):
            binding = get_best_binding(event)
            if binding:
                binding.handler(binding.trigger, event)
            return False

        return handler

    def __init__(self, key: Key, collection: KeyBindingCollection):
        self.key = key
        self._collection = collection
        self.manufactured_handler = self._get_handler()

    def __enter__(self):
        self._internal_handler = hook_key(
            _get_keyboard_hook_id(self.key), self.manufactured_handler, suppress=True
        )
        return self

    def __exit__(self):
        unhook(self._internal_handler)
        return self


def _get_keyboard_hook_id(key: Key) -> str:
    match key.id:
        case "num enter":
            return "enter"
        case "num dot" | "num .":
            return "."
        case "num star" | "num *" | "num multiply":
            return "*"
        case "num plus" | "num +":
            return "+"
        case "num minus" | "num -":
            return "-"
        case "num slash" | "num /":
            return "/"
        case "mouse 1":
            return "left"
        case "mouse 2":
            return "right"
        case "mouse 3":
            return "middlemouse"
        case "mouse 4":
            return "x"
        case "mouse 5":
            return "x2"
        case _:
            return key.id


def _get_windows_id_for_mouse_key(key: Key) -> int:
    if key.is_mouse:
        return int(key.id.replace("mouse ", ""))
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
