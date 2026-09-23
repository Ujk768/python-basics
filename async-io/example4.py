import asyncio
import time


async def fetch_data(param):
    print(f"Do something with {param}...")
    await asyncio.sleep(param)
    print(f"Done with {param}")
    return f"Result of {param}"


async def main():
    task1 = asyncio.create_task(fetch_data(1))
    task2 = asyncio.create_task(fetch_data(2))
    result2 = await task2
    print("Task 2 fully completed")
    result1 = await task1
    print("Task 1 fully completed")
    return [result1, result2]


t1 = time.perf_counter()

results = asyncio.run(main())
print(results)

t2 = time.perf_counter()
print(f"Finished in {t2 - t1:.2f} seconds")


# main co routine gets created
# fetch_data(1) coroutine is created and scheduled on the event loop
# fetch_data(2) co routine is created and scheduled on the event loop
# await task 2 suspends the main co routine . co routine 1 and co routine 2 are in ready state
# it picks up co routine 1 and starts executing it
# await asyncio.sleep(1) causes co routine 1 to be suspended. A timer runs in the background for 1 sec
# main and co routine 1 are suspended so event loop picks up co routine 2 and starts its execution
# co routine 2 reaches await asyncio.sleep(2) and is suspended
# At this point all 3 coroutines are suspended
# timer for 1 sec completes and coroutine 1 is awakened and it starts running till its finished
# timer for 2 sec is completed and coroutine 2 completes which awakens the main co routine
# main now continues and reaches await for task1
# since that task was akready completed it simply returns its value directly and execution of main continues
# main co routine is complete and we get all the results



# Key asyncio concepts:
#
# 1. asyncio.create_task(coro)
#    - Schedules the coroutine to be run by the event loop.
#    - It does NOT necessarily execute the coroutine immediately.
#    - Once multiple tasks are scheduled, the event loop can switch between them.
#
# 2. await task
#    - Suspends ONLY the current coroutine until the awaited task is complete.
#    - It does NOT stop the event loop or prevent other tasks from running.
#    - It also does NOT give the awaited task priority.
#
# 3. await asyncio.sleep(n)
#    - Suspends the current coroutine for n seconds.
#    - Control is returned to the event loop.
#    - The event loop can run other ready tasks while this coroutine is waiting.
#
# 4. Scheduling order vs await order
#    - create_task() determines which coroutines are scheduled for execution.
#    - The order of await statements determines when the CURRENT coroutine
#      (e.g. main) is allowed to continue.
#    - await task2 does NOT mean "run task2 before task1".
#
# Example:
#
# task1 = asyncio.create_task(fetch_data(1))
# task2 = asyncio.create_task(fetch_data(2))
#
# result2 = await task2
# result1 = await task1
#
# Both task1 and task2 are scheduled before main waits for task2.
#
# main pauses at "await task2", but the event loop can still run task1 and task2.
#
# If task1 sleeps for 1 second and task2 sleeps for 2 seconds:
#
#   t=0   task1 starts → sleep(1) → pauses
#         task2 starts → sleep(2) → pauses
#
#   t=1   task1 wakes up → finishes
#
#   t=2   task2 wakes up → finishes
#         main resumes because task2 is now complete
#
#         main gets result2
#         main awaits task1
#         task1 is already complete, so main continues immediately
#
# Therefore:
#
#   "await task2" means:
#       "main cannot continue until task2 finishes"
#
#   NOT:
#       "task2 must execute before task1"
#
# The core mental model:
#
#   create_task() → makes work available to the event loop
#   await         → pauses the current coroutine
#   event loop    → runs other tasks while the current coroutine is waiting
#
# Asyncio uses cooperative concurrency:
# coroutines voluntarily give control back to the event loop when they await.