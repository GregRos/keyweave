from typing import Any, Iterable


from pykeys.bindings import BindingCollection, HotkeyInterceptor
from pykeys.bindings import Binding
from pykeys.commanding import Command, CommandProducer, resolve_command
from pykeys.hotkey import Hotkey
from pykeys.key_types import Key
from pykeys.hook import KeyHook
from pykeys.schedulers import default_scheduler, Scheduler


class Layout:
    _registered: list[KeyHook]
    _map: BindingCollection
    _active: bool = False

    def __init__(
        self,
        name: str,
        scheduler: Scheduler | None = None,
        bindings: Iterable[Binding] = (),
    ):
        def on_error(e: BaseException):
            print(f"Error: {e}")

        scheduler = scheduler or default_scheduler(on_error)
        self.name = name
        self._scheduler = scheduler
        self._map = BindingCollection()
        for binding in bindings:
            self.add_binding(binding)

    def __iadd__(self, binding: Binding):
        self.add_binding(binding)
        return self

    @property
    def is_empty(self):
        return len(self._map) == 0

    def intercept(self, interceptor: HotkeyInterceptor):
        return Layout(
            self.name,
            self._scheduler,
            [binding.intercept(interceptor) for binding in self._map.bindings],
        )

    @property
    def active(self):
        return self._active

    def add_binding(self, binding: Binding):
        self._map += binding

    def __len__(self):
        return len(self._map)

    def __iter__(self):
        return iter(self._map)

    @property
    def bindings(self):
        return self._map.bindings

    def _get_key_hooks(self):
        return [
            KeyHook(key, bindings, self._scheduler)
            for key, bindings in self._map.pairs
        ]

    def __enter__(self):
        from .print_layout import print_layout_table

        print(f"➡️ {print_layout_table(self)}")
        key_hooks = self._get_key_hooks()
        registered: list[KeyHook] = []
        try:
            for hook in key_hooks:
                hook.__enter__()
                registered.append(hook)
        except:
            for hook in registered:
                hook.__exit__()
            raise
        self._registered = key_hooks

    def __exit__(self, *args: Any):
        for hook in self._registered:
            hook.__exit__()
        return False

    @staticmethod
    def create(
        name: str, d: dict[Hotkey | Key, Command | CommandProducer]
    ) -> "Layout":
        clean_dict = {
            (k.down if isinstance(k, Key) else k): v for k, v in d.items()
        }
        xs = [
            Binding(k.info, resolve_command(v, None))
            for k, v in clean_dict.items()
        ]
        return Layout(name, bindings=xs)
