from logging import Handler
from typing import Any
from pykeys.compound_binding import CompoundBinding
from pykeys.key import Key
from pykeys.key_combination import KeyCombination
from pykeys.layout import Layout
from pykeys.trigger_combination import TriggerCombination

type BindingDict = dict[TriggerCombination, Handler]

def hotkey(combination: TriggerCombination | Key | KeyCombination):
    def wrapper[X](func: X) -> X:
        bindings = func.__dict__.setdefault("bindings", set[TriggerCombination]())
        bindings.add(combination)
        return func

    return wrapper


def hotkey_layout(cls: type) -> Layout:
    layout = Layout(cls.__name__)
    any_found = False
    for func in cls.__dict__.values():
        if callable(func) and hasattr(func, "bindings"):
            dt: dict[] = func.__dict__.bindings
            for binding in func["bindings"]:
                layout.add_bindings(binding.trigger, binding)
            any_found = True

    if not any_found:
        raise ValueError(f"No bindings found in {cls}")
    return layout


class LayoutClass(type):
    def register(self):
        
    def __new__(cls, name: str, bases: list[type], dct: dict[str, Any]):
        layout = Layout(name)
        bindings_by_trigger: BindingDict = {}
        for func in dct.values():
            bindings: list[TriggerCombination | Key | KeyCombination] = func["bindings"]
            if isinstance(func, dict) and bindings:
                for binding in bindings:
                    layout.add_bindings(CompoundBinding())
                any_found = True

        if not any_found:
            raise ValueError(f"No bindings found in {cls}")
        return layout


@hotkey_layout
class Something:
    pass
