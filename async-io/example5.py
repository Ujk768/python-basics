import asyncio
import time


async def fetch_data(param):
    print(f"Do something with {param}...")
    # instead of using asynio.sleep we are using time.sleep which is synchronous
    time.sleep(param)
    print(f"Done with {param}")
    return f"Result of {param}"


async def main():
    task1 = asyncio.create_task(fetch_data(1))
    task2 = asyncio.create_task(fetch_data(2))
    result1 = await task1
    print("Task 1 fully completed")
    result2 = await task2
    print("Task 2 fully completed")
    return [result1, result2]


t1 = time.perf_counter()

results = asyncio.run(main())
print(results)

t2 = time.perf_counter()
print(f"Finished in {t2 - t1:.2f} seconds")



# since we are calling sync code inside the event loop we are essentially blocking the event loop 
# intially we create both the co routines and they are scehduled and added on the event loop.
# when we await fetch_data(1) it stops the main co routine and starts the execution of fetch_Data(1)
# fetch_Data(1) pauses cause of sync code and no other co routines start
# once fetch_Data(1) completes we and our main co routine is also ready but because of FIFO  we start execution of the second co routine
# the second co routine runs and is paused for  2 seconds and then completes and main co routine runs again
# finally the main finishes and he results are returned.
# because we cant await the co rotuines they run sequentially and we cant run the benefits of parallel execution