from functools import partial

import uvicorn
import threading
import signal

from fastapi import FastAPI

from routers.constants import ROUTE_PREFIX
from routers.routes import core_router
from routers.util_routes import util_router
from settings.config import settings
from settings.logging_config import produce_logger
from tasks_framework.app import worker, task_queue
from multiprocessing.pool import Pool


_logger = produce_logger(__name__)

app = FastAPI()

app.include_router(prefix=ROUTE_PREFIX, router=core_router)
app.include_router(prefix=ROUTE_PREFIX, router=util_router)


def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)


if __name__ == "__main__":
    pool = Pool(processes=2, initializer=init_worker)
    worker_thread = threading.Thread(target=partial(worker, pool))
    _logger.info("Initializing worker thread")
    worker_thread.start()
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT)
    task_queue.put(("__stop__", None, None))
    worker_thread.join()
    pool.close()
    pool.join()
