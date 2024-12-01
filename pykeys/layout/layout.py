from typing import Iterable


from pykeys.bindings.binding_collection import BindingCollection
from pykeys.bindings.trigger_binding import Binding
from pykeys.bindings.interception import ActionInterceptor
from pykeys.layout.key_hook import KeyHook
from pykeys.schedulers.default import default_scheduler
from pykeys.schedulers.scheduling import Scheduler


# KEY | MODIFIERS
#
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

    def intercept(self, interceptor: ActionInterceptor):
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
            KeyHook(key, bindings, self._scheduler) for key, bindings in self._map.pairs
        ]

    def __enter__(self):
        from .print_layout import get_layout_table

        print(f"➡️ {get_layout_table(self)}")
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

    def __exit__(self):
        for hook in self._registered:
            hook.__exit__()
