import asyncio
import time
from concurrent.futures import ProcessPoolExecutor


def fetch_data(param):
    print(f"Do something with {param}...", flush=True)
    time.sleep(param)
    print(f"Done with {param}", flush=True)
    return f"Result of {param}"


async def main():
    # Run in Threads - we dont call the fuinction here like [fetch_data(1)] becuase we want to just schedule the sync code and run it later 
    task1 = asyncio.create_task(asyncio.to_thread(fetch_data, 1))
    task2 = asyncio.create_task(asyncio.to_thread(fetch_data, 2))
    result1 = await task1
    print("Thread 1 fully completed")
    result2 = await task2
    print("Thread 2 fully completed")

    # Run in Process Pool
    loop = asyncio.get_running_loop()

    with ProcessPoolExecutor() as executor:
        task1 = loop.run_in_executor(executor, fetch_data, 1)
        task2 = loop.run_in_executor(executor, fetch_data, 2)
        result1 = await task1
        print("Process 1 fully completed")
        result2 = await task2
        print("Process 2 fully completed")

    return [result1, result2]



# this makes cure this runs only for the main orocess and not for the other child processes that are running
if __name__ == "__main__":
    t1 = time.perf_counter()

    results = asyncio.run(main())
    print(results)

    t2 = time.perf_counter()
    print(f"Finished in {t2 - t1:.2f} seconds")


  # create and schedule co routines onto the event loop
  # awaiting task 1 which is a process that runs in the background and the main process is suspended
  # since its a waits for the other process to complete this coroutine is suspended
  # it runs the next co routine which runs on another process in the background 
  # once the first proces is complete the main co routine is active again and it runs  and waits for the second task to finish
  # once the second task finishes  it then completes the main co routine

