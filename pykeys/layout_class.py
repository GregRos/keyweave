from pykeys.key import Key
from pykeys.key_combination import KeyCombination
from pykeys.layout import Layout
from pykeys.trigger_combination import TriggerCombination


def hotkey[X](combination: TriggerCombination | Key | KeyCombination) -> X:
    def wrapper(func: X) -> X:
        func.__dict__.setdefault("bindings", []).append(combination)
        return func

    return wrapper


def hotkey_layout(cls: type) -> Layout:
    layout = Layout(cls.__name__)
    any_found = False
    for func in cls.__dict__.values():
        if isinstance(func, dict) and "bindings" in func:
            for binding in func["bindings"]:
                layout.add_bindings(binding.trigger, binding)
            any_found = True

    if not any_found:
        raise ValueError(f"No bindings found in {cls}")
    return layout


class LayoutClass(type):
    def __new__(cls, name, bases, dct):
        layout = Layout(name)
        any_found = False
        for func in dct.values():
            if isinstance(func, dict) and "bindings" in func:
                for binding in func["bindings"]:
                    layout.add_bindings(binding.trigger, binding)
                any_found = True

        if not any_found:
            raise ValueError(f"No bindings found in {cls}")
        return layout


@hotkey_layout
class Something:
    pass


a = Something
