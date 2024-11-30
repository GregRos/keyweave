from typing import Protocol


class ScheduleItem(Protocol):
    def __call__(self) -> None: ...


class Scheduler(Protocol):

    def __call__(self, func: ScheduleItem, /) -> None: ...


class ScheduleErrorHandler(Protocol):
    def __call__(self, error: BaseException, /) -> None: ...
