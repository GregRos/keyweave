from dataclasses import dataclass


from pykeys.keys.cmd import Act
from pykeys.keys.key_trigger import KeyTrigger


@dataclass(match_args=True)
class TriggerBinding:
    trigger: KeyTrigger
    act: Act
