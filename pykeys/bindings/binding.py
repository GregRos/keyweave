from dataclasses import dataclass, field
import inspect


from pykeys.bindings.interceptor import (
    HotkeyInterceptor,
    HotkeyInterceptionEvent,
)
from pykeys.commanding.event import InputEvent, HotkeyEvent
from pykeys.commanding.handler import FuncHotkeyHandler
from pykeys.key.hotkey import HotkeyInfo
from pykeys.commanding.command import Command
