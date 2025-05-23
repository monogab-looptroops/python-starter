import asyncio
import time

"""
This example shows how to run basic async functions
"""

async def print_1():
    print("1")
    await asyncio.sleep(1)
    print("1 Done")


async def print_2():
    print("2")
    await asyncio.sleep(1)
    print("2 Done")


async def main_concurrent_tasks():
    """
    Make sure you keep a reference to each task and then await it.
    If we keep no reference to each task, it might be garbage collected by python at any moment, preventing it from running.
    Use TaskGroup instead for python version 3.11 and above!
    """
    task1 = asyncio.create_task(print_1())
    task2 = asyncio.create_task(print_2())

    print(f"started at {time.strftime('%X')}")

    # Wait until both tasks are completed
    await task1
    await task2

    print(f"finished at {time.strftime('%X')}")


async def main_concurrent_taskgroup():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(print_1())

        task2 = tg.create_task(print_2())

        print(f"started at {time.strftime('%X')}")

    # The await is implicit when the context manager exits.

    print(f"finished at {time.strftime('%X')}")


async def main_ordered():
    print(f"started at {time.strftime('%X')}")
    await print_1()
    await print_2()
    print(f"finished at {time.strftime('%X')}")

asyncio.run(main_concurrent_tasks())
asyncio.run(main_concurrent_taskgroup())
asyncio.run(main_ordered())
