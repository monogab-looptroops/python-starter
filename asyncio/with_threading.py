"""
This example shows how to combine Sync and Async code by running the sync code in a separate executor.
Data can be shared across these classes.
"""

import concurrent.futures
import threading
import time
import asyncio, concurrent


class SyncClass:
    """
    A class that runs synchronous code (in a thread)
    """
    def __init__(self, name) -> None:
        self.counter = 0
        self.name = name

    def start(self, print_data=True):
        threading.Thread(target=self.print_counter, args=[print_data]).start()

    def print_counter(self, print_data):
        while True:
            if print_data:
                print(f"Sync counter for {self.name} is at {self.counter}")
            self.counter = self.counter + 1
            time.sleep(1)


class AsyncClass:
    """
    A class that runs asynchronous code
    """
    def __init__(self, name, other_class_reference: SyncClass) -> None:
        self.counter = 0
        self.name = name
        self.other_class_reference: SyncClass = other_class_reference

    async def start(self):
        await self.print_counter()

    async def print_counter(self):
        while True:
            print(f"Async counter for {self.name} is at {self.counter}")
            print(f"I can read the counter from the sync class. It is at {self.other_class_reference.counter}")
            self.counter = self.counter + 1
            await asyncio.sleep(0.5)


async def run_tasks():
    sync_class = SyncClass("SyncClass")
    async_class = AsyncClass("AsyncClass", sync_class)

    executor = concurrent.futures.ThreadPoolExecutor()
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(executor, sync_class.start, False)

    async with asyncio.TaskGroup() as tg:
        task = tg.create_task(async_class.start())


asyncio.run(run_tasks())
