from concurrent.futures import ThreadPoolExecutor
from typing import Protocol
from pykeys.schedulers.scheduling import ScheduleItem, Scheduler


class ScheduleErrorHandler(Protocol):
    def __call__(self, error: Exception) -> None: ...


class DefaultScheduler(Scheduler):
    _pool: ThreadPoolExecutor

    def __init__(self, on_error):5
        self._pool = ThreadPoolExecutor(1)

    def __call__(self, func: ScheduleItem) -> None:
        f = self._pool.submit(func)A
