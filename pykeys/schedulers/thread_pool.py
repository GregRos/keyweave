from concurrent.futures import ThreadPoolExecutor
from typing import Callable
from pykeys.keys.key import Key
from pykeys.layout.scheduling import ScheduleItem, Scheduler


class ThreadPoolScheduler(Scheduler):
    _pool: ThreadPoolExecutor

    def __init__(self):
        self._pool = ThreadPoolExecutor(1)

    def __call__(self, func: ScheduleItem) -> None:
        self._pool.submit(func)
