import asyncio
import time


async def fetch_data(param):
    print(f"Do something with {param}...")
    await asyncio.sleep(param)
    print(f"Done with {param}")
    return f"Result of {param}"


async def main():
    # We are creating tasks now which are scheduled to run these task on the event loop
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

#  Run creates an event loop and starts the main co routine -> event loop starts executing main
#  create.task for task 1 is called and fetch_data(1) co routine is scheduled and put on the event loop in state ready -> it still executes main co routine
#  create.task for task 2 is called and fetch_data(2) co routine is scheduled and put on the event loop. Its also in ready state -> still main co routine executes
#  await task 1 -> will now  start executing fetch_data(1) co routine and main co routine goes to sleep
#  Task 1 reaches await asyncio.sleep and it suspends the running and it goes to sleep
#  Now both main coroutine and task 1 coroutine are suspended so event loop checks to see if there are any tasks and it finds task2
#  Task 2 co routine is started and it hits await which suspends fetch_data(2) until asyncio.sleep is done
#  Timer 1 completes and fetch_data(1) is woken up and it compeltes and wakes up main co routine
#  main co routine continues execution and now it waits for completion of task 2 -> which has already started and is suspended
#  It waits for timer 2 to complete and wakes up fetch_data(2) co routine
#  Event loop finishes executing task2 co routine and starts the main after its complete
# now main has results from both co routines and prints the results and finishes its execution

##  We scheduled the tasks ahead of time and while one background task was running we satrted the next coroutine when both main 
# and task 1 co routines were suspended




