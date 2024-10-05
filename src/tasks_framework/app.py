import asyncio
import datetime
import multiprocessing
import functools
from concurrent.futures import ProcessPoolExecutor

from models.config import get_db_session
from settings.logging_config import produce_logger
from time import perf_counter
from managers.tasks_sql_manager import TasksSQLManager

task_queue = multiprocessing.Queue()
registered_tasks = {}

_logger = produce_logger(__name__)


async def _update_state_shortcut(
    instance_id: str,
    data: dict[str, datetime.datetime | float | str]
):
    async with get_db_session() as session:
        await TasksSQLManager(session).update(instance_id, data)
        await session.commit()


def task(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(_update_state_shortcut(
            instance_id=kwargs["_task_id"],
            data={
                "start_time": datetime.datetime.now(datetime.UTC),
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
    registered_tasks[func.__name__] = func

    async def delay(*args, **kwargs):
        async with get_db_session() as session:
            instance = await TasksSQLManager(session).create(data=None)
            kwargs["_task_id"] = instance.id
            task_queue.put_nowait((func.__name__, args, kwargs))
            await session.commit()
        return kwargs["_task_id"]
    wrapper.delay = delay
    return wrapper


async def main(num_workers: int = 2):
    with ProcessPoolExecutor(max_workers=num_workers, ) as executor:
        while True:
            _logger.info("Waiting for tasks...")
            func_name, args, kwargs = task_queue.get()
            task_id = kwargs["_task_id"]
            _logger.info(f"Received task {task_id}")
            if func_name in registered_tasks:
                executor.submit(
                    registered_tasks[func_name],
                    *args,
                    **kwargs
                )
            else:
                _logger.error(f"No task found with name: {func_name}")


if __name__ == "__main__":
    asyncio.run(main())
