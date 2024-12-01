from dataclasses import dataclass, field
import inspect


from pykeys.bindings.interceptor import ActionInterceptor, InterceptedAction
from pykeys.commanding.event import InputEvent, HotkeyEvent
from pykeys.commanding.handler import Handler
from pykeys.key.hotkey import Hotkey
from pykeys.commanding.command import Command


@dataclass(match_args=True)
class Binding:
    hotkey: Hotkey
    handler: Handler
    metadata: Command
    _number_of_args: int = field(init=False)

    def __post_init__(self):
        self._number_of_args = len(inspect.signature(self.handler).parameters)
        if not callable(self.handler):
            raise ValueError(f"handler must be a callable, got {self.handler}")
        if self._number_of_args != 1:
            raise ValueError(
                f"handler must accept 1 argument, got {self._number_of_args}"
            )

    def intercept(self, *interceptors: ActionInterceptor):
        handler = self.handler
        for interceptor in interceptors:
            handler = _wrap_interceptor(interceptor, handler)
        return Binding(self.hotkey, handler, self.metadata)

    def __call__(self, event: InputEvent, /):
        handler = self.handler
        triggered_key_event = HotkeyEvent(self.hotkey, event)
        handler(triggered_key_event)


def _wrap_interceptor(interceptor: ActionInterceptor, handler: Handler) -> Handler:
    def _handler(e: HotkeyEvent):
        interception = InterceptedAction(e, handler)
        interceptor(interception)
        if not interception.handled:
            raise ValueError(f"Interceptor {interceptor} did not handle {e}")

    return _handler
