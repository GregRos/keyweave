from dataclasses import dataclass

from pykeys.schedulers.scheduling import ScheduleErrorHandler
from pykeys.schedulers.threadpool import ThreadPoolScheduler


def default_scheduler(on_error: ScheduleErrorHandler):
    return ThreadPoolScheduler(workers=1, on_error=on_error)
