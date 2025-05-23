"""
This example shows a synchronous subprocess that runs in a thread executor.
It shows how to raise the exception from the subprocess and catch it in the main asyncio event loop.
"""
import asyncio
import concurrent.futures


def raise_some_errors():
    try:
        0 / 0
    except Exception as e:
        raise e

async def main():
    loop = asyncio.get_running_loop()    
    while True:
        try:
            with concurrent.futures.ThreadPoolExecutor() as executor:
            # Be sure to await here, or you will get an error like 'Future exception was never retrieved'
                await loop.run_in_executor(executor, raise_some_errors)
        except Exception as e:
            print(f"Exception raised: {e}")
        await asyncio.sleep(1)

asyncio.run(main())