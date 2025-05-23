"""
This class shows how to combine serveral concepts and use them in a fastapi context.
It also shows how to use asyncio to call API endpionts (by calling our own endpoints). 
"""

import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, BackgroundTasks
import uvicorn
import aiohttp
import time
import concurrent.futures


def slow_sync_function(generate_exception=False):
    print("Starting slow sync function")
    if generate_exception:
        0 / 0
    time.sleep(5)
    print("Stopping slow sync function")
    return "I am done"


class AsyncCounter:
    def __init__(self) -> None:
        self.counter = 0
        self.run = True

    async def start(self):
        print("Starting loop")
        while self.run:
            await asyncio.sleep(1)
            self.counter = self.counter + 1
            print(f"Counter is {self.counter}")

    def stop(self):
        print("Now stopping loop")
        self.run = False


async_counter = AsyncCounter()
session: aiohttp.ClientSession = None


"""
Start background processes here
"""


async def run_tasks():
    async with asyncio.TaskGroup() as tg:
        task = tg.create_task(async_counter.start())


"""
FastApi lifespan hook to start background tasks
"""


@asynccontextmanager
async def lifespan(app: FastAPI):
    global session

    # Load the tasks
    tasks = asyncio.create_task(run_tasks())
    session = aiohttp.ClientSession()
    yield
    # Clean up and release the resources
    await session.close()
    async_counter.stop()


app = FastAPI(lifespan=lifespan)


@app.get("/getCounter")
async def get_counter(testVar: bool = True):
    return {
        "counter": async_counter.counter,
        "test_var": testVar,
    }


@app.get("/getCounterSlow")
async def get_counter_slow():
    """
    This endpoint introduces an await to simulate a slow response from an api
    """
    await asyncio.sleep(5)
    return {"counter": async_counter.counter}


@app.get("/getCounterThroughApi")
async def get_counter_through_api(testVar: bool = True):
    """
    Here, we call our own api to get the counter value
    !!!!! Make sure you cast booleans to strin !!!!!
    """
    response = await session.get(
        "http://localhost:5000/getCounter",
        params={"testVar": str(testVar)},
    )
    print(f"Response ok is {response.ok}")
    return await response.json()


@app.get("/getCounterThroughApiSlow")
async def get_counter_through_api_slow():
    """
    Here, we call our own api to get the counter value but use the slow endpoint
    """
    response = await session.get("http://localhost:5000/getCounterSlow")
    return await response.json()


# session = aiohttp.ClientSession()


@app.get("/getCounterThroughApiTimeout")
async def get_counter_through_api_slow_timeout():
    """
    Here, we raise a timeout
    """
    try:
        response = await session.get("http://localhost:5000/getCounterSlow", timeout=1)
        return await response.json()
    except asyncio.TimeoutError:
        raise HTTPException(status_code=408, detail="Request timed out")
    except Exception as e:
        print(f"Exception: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/runBackgroundTask")
async def run_background_task(background_tasks: BackgroundTasks):
    background_tasks.add_task(slow_sync_function)


@app.get("/getSyncFunctionResult")
async def get_sync_function_result(generate_exception: bool = False):
    loop = asyncio.get_running_loop()
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Be sure to await here, or you will get an error like 'Future exception was never retrieved'
            result = await loop.run_in_executor(executor, slow_sync_function, generate_exception)
            return result
    except Exception as e:
        print(f"Exception: {e}")
        raise HTTPException(status_code=400, detail=str(e))


uvicorn.run(app, host="0.0.0.0", port=5000)
