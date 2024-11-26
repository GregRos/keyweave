from concurrent.futures import ThreadPoolExecutor
from pykeys.layout.scheduling import ScheduleItem, Scheduler


class DefaultScheduler(Scheduler):
    _pool: ThreadPoolExecutor

    def __init__(self):
        self._pool = ThreadPoolExecutor(1)

    def __call__(self, func: ScheduleItem) -> None:
        self._pool.submit(func)
