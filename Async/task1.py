import asyncio
import random
from typing import List

MAX_SEMAPHORE_NUMBER = 5
WORKERS_NUMBER = 5
TASKS_NUMBER = 100


def generate_tasks() -> List:
    tasks = [
        {"task_id": i, "duration": random.uniform(0.5, 2.0)} for i in range(1, TASKS_NUMBER + 1)
    ]
    return tasks


async def worker(worker_id: int, queue: asyncio.Queue, semaphore: asyncio.Semaphore) -> None:
    """Creates worker. Worker is ready to do tasks."""

    while True:
        task = await queue.get()
        async with semaphore:
            task_id = task["task_id"]
            duration = task["duration"]
            print(f"Worker {worker_id} -> Task {task_id} starts (duration: {duration} ms)")
            await asyncio.sleep(duration)
            print(f"Worker {worker_id} -> Task {task_id} finished")
        queue.task_done()


async def main() -> None:
    queue = asyncio.Queue()
    semaphore = asyncio.Semaphore(MAX_SEMAPHORE_NUMBER)

    tasks = generate_tasks()

    for task in tasks:
        await queue.put(task)

    # creating workers ready to work
    workers = [
        asyncio.create_task(worker(w_id, queue, semaphore)) for w_id in range(1, WORKERS_NUMBER + 1)
    ]

    await queue.join()

    #  release workers so that they don't get stuck
    for w in workers:
        w.cancel()

    await asyncio.gather(*workers)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except asyncio.exceptions.CancelledError:
        print("Finished")