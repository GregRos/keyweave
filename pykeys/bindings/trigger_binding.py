from dataclasses import dataclass, field
import inspect
from typing import Callable


from pykeys.bindings.interception import ActionInterceptor, InterceptedAction
from pykeys.commanding.event import KeyEvent
from pykeys.commanding.handler import Handler
from pykeys.key.key_trigger import KeyTrigger
from pykeys.commanding.metadata import Command


@dataclass(match_args=True)
class CommandBinding:
    trigger: KeyTrigger
    handler: Handler
    metadata: Command
    _number_of_args: int = field(init=False)

    def __post_init__(self):
        self._number_of_args = len(inspect.signature(self.handler).parameters)
        if not callable(self.handler):
            raise ValueError(f"handler must be a callable, got {self.handler}")
        if self._number_of_args != 2:
            raise ValueError(
                f"handler must accept 2 arguments, got {self._number_of_args}"
            )

    def intercept(self, *interceptors: ActionInterceptor):
        handler = self.handler
        for interceptor in interceptors:
            handler = _wrap_interceptor(interceptor, handler)
        return CommandBinding(self.trigger, handler, self.metadata)

    def __call__(self, event: KeyEvent, /):
        handler = self.handler
        handler(self.trigger, event)


def _wrap_interceptor(interceptor: ActionInterceptor, handler: Handler) -> Handler:
    def _handler(trigger: KeyTrigger, event: KeyEvent):
        interception = InterceptedAction(trigger, event, handler)
        interceptor(interception)
        if not interception.handled:
            raise ValueError(
                f"Interceptor {interceptor} did not handle {trigger}@{event}"
            )

    return _handler
