from taskiq import TaskiqScheduler, ScheduleSource, AsyncBroker

from pix_erase.setup.bootstrap import setup_schedule_source, setup_scheduler
from pix_erase.setup.config.settings import AppConfig
from pix_erase.worker import create_worker_taskiq_app


def create_scheduler_taskiq_app() -> TaskiqScheduler:
    configs: AppConfig = AppConfig()
    task_iq_app: AsyncBroker = create_worker_taskiq_app()
    schedule_source: ScheduleSource = setup_schedule_source(configs.redis)
    scheduler: TaskiqScheduler = setup_scheduler(broker=task_iq_app, schedule_source=schedule_source)
    return scheduler
