from typing import Callable

from pykeys.trigger_info import TriggerInfo


type Handler = Callable[[TriggerInfo], None]
