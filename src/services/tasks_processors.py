import random
import time

from settings.logging_config import produce_logger
from tasks_framework.app import task


_logger = produce_logger(__name__)


@task
def process(*args, **kwargs):
    _logger.info(f"Processing task {kwargs['_task_id']}")
    time.sleep(random.randint(0, 10))
    _logger.info("Finished")
