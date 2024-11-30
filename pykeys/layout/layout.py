from typing import Iterable


from pykeys.bindings.binding_collection import BindingCollection
from pykeys.commanding.event import KeyEvent
from pykeys.commanding.handler import Handler
from pykeys.commanding.trigger_binding import CommandBinding
from pykeys.key.key_trigger import KeyTrigger
from pykeys.layout.interception import ActionInterceptor, InterceptedAction
from pykeys.layout.key_hook import KeyHook
from pykeys.schedulers.scheduling import Scheduler


# KEY | MODIFIERS
#
class Layout:
    _registered: list[KeyHook]
    _map: BindingCollection
    _active: bool = False

    def __init__(
        self, name: str, scheduler: Scheduler, bindings: Iterable[CommandBinding] = ()
    ):
        self.name = name
        self._scheduler = scheduler
        self._map = BindingCollection()
        for binding in bindings:
            self.add_binding(binding)

    def __iadd__(self, binding: CommandBinding):
        self.add_binding(binding)
        return self

    @property
    def is_empty(self):
        return len(self._map) == 0

    def intercept(self, interceptor: ActionInterceptor):
        def _intercept_handler(handler: Handler):
            def _handler(trigger: KeyTrigger, event: KeyEvent):
                interception = InterceptedAction(trigger, event, handler)
                interceptor(interception)
                if not interception.handled:
                    raise ValueError(
                        f"Interceptor {interceptor} did not handle {trigger}@{event}"
                    )

            return _handler

        return Layout(
            self.name,
            self._scheduler,
            [b.map(_intercept_handler) for b in self._map.bindings],
        )

    @property
    def active(self):
        return self._active

    def add_binding(self, binding: CommandBinding):
        self._map += binding

    def __len__(self):
        return len(self._map)

    def __iter__(self):
        return iter(self._map)

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
