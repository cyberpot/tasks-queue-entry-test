import asyncio
import datetime
import functools
import queue
import importlib
import traceback
from multiprocessing.pool import Pool

from models.config import context_db_session
from settings.logging_config import produce_logger
from time import perf_counter
from managers.tasks_sql_manager import TasksSQLManager

task_queue = queue.Queue()
registered_tasks = []

_logger = produce_logger(__name__)


def get_function_from_string(func_name: str):
    module_name, func_name = func_name.rsplit('.', 1)
    module = importlib.import_module(module_name)
    return getattr(module, func_name)


async def _update_state_shortcut(
    instance_id: str,
    data: dict[str, datetime.datetime | float | str]
):
    async with context_db_session() as session:
        await TasksSQLManager(session).update(instance_id, data)
        await session.commit()


def task(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(_update_state_shortcut(
            instance_id=kwargs["_task_id"],
            data={
                "start_time": datetime.datetime.now(),
            }
        ))
        start_exec = perf_counter()
        result = func(*args, **kwargs)
        loop.run_until_complete(_update_state_shortcut(
            instance_id=kwargs["_task_id"],
            data={
                "exec_time": perf_counter() - start_exec
            }
        ))
        return result
    registered_tasks.append(func.__module__ + "." + func.__name__)

    async def delay(*args, **kwargs):
        async with context_db_session() as session:
            instance = await TasksSQLManager(session).create(data=None)
            kwargs["_task_id"] = instance.id
            task_queue.put_nowait((
                func.__module__ + "." + func.__name__, args, kwargs
            ))
            await session.commit()
        return kwargs["_task_id"]
    wrapper.delay = delay
    return wrapper


def worker(pool: Pool):
    while True:
        func_name, args, kwargs = task_queue.get()
        if func_name == "__stop__":
            _logger.info("Stopping...")
            break
        task_id = kwargs["_task_id"]
        _logger.info(f"Received task {task_id}")
        if func_name in registered_tasks:
            try:
                pool.apply_async(
                    get_function_from_string(func_name),
                    args,
                    kwargs
                )
            except Exception:
                _logger.error(f"Can`t put task {kwargs['_task_id']} in the queue")
                _logger.error(traceback.format_exc())
                continue
        else:
            _logger.error(f"No task found with name: {func_name}")
