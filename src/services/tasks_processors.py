import random
import time
from tasks_framework.app import task


@task
def process(*args, **kwargs):
    time.sleep(random.randint(0, 10))
