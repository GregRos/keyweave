from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass, field
from pykeys.schedulers.scheduling import ScheduleErrorHandler, ScheduleItem, Scheduler


@dataclass(kw_only=True)
class ThreadPoolScheduler(Scheduler):
    on_error: ScheduleErrorHandler
    workers: int
    _pool: ThreadPoolExecutor = field(init=False)

    def __post_init__(self):
        self._pool = ThreadPoolExecutor(max_workers=self.workers)

    def __call__(self, func: ScheduleItem) -> None:
        def callback(f: Future[None]):
            if ex := f.exception():
                self.on_error(ex)
            return object()

        self._pool.submit(func).add_done_callback(callback)
