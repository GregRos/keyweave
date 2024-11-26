from typing import Protocol


class ScheduleItem(Protocol):
    def __call__(self) -> None: ...


class Scheduler(Protocol):

    def __call__(self, func: ScheduleItem) -> None: ...
