from dataclasses import dataclass
from typing import Callable

from keyboard import KeyboardEvent

from pykeys.keys.key_trigger import KeyTrigger

type Handler = Callable[[KeyTrigger, KeyboardEvent] | [KeyTrigger] | [], None]


@dataclass(match_args=True)
class TriggerBinding:
    trigger: KeyTrigger
    handler: Handler
    label: str
    description: str = ""
