import asyncio
import time


async def fetch_data(param):
    print(f"Do something with {param}...")
    await asyncio.sleep(param)
    print(f"Done with {param}")
    return f"Result of {param}"


async def main():
    task1 = fetch_data(1)  # Could be awaited directly
    task2 = fetch_data(2)  # Could be awaited directly
    # We are scheduling and running the co routine together at the same time 
    result1 = await task1
    print("Task 1 fully completed")
    # We are scheduling and running the co routine at the same time
    result2 = await task2
    print("Task 2 fully completed")
    return [result1, result2]


t1 = time.perf_counter()

results = asyncio.run(main())
print(results)

t2 = time.perf_counter()
print(f"Finished in {t2 - t1:.2f} seconds")


# This still takes the same time approx 3 seconds 
#  Main co routine executes
# reaches await fetch_data(1)

# fetch_data(1) co routine is schedled and runs immeadiately , Main co routine is suspended and goes to sleep
# it reaches await asyncio.sleep(1) -> fetch_data(1) co routine is suspended and goes to sleep
# goes to background process and sleeps for 1 sec 
# background process is completed and wakes up fetch_data(1) co routine
# fetch_data(1) co routine then completes and wakes up main

# Main co routine executes
# reaches await fetch_data(2)
# fetch_data(2) co routine is schedled and runs immeadiately , Main co routine is suspended and goes to sleep
# it reaches await asyncio.sleep(2) -> fetch_data(2) co routine is suspended and goes to sleep
# goes to background process and sleeps for 2 sec 
# background process is completed and wakes up fetch_data(2) co routine
# fetch_data(2) co routine then completes and wakes up main

# main then prints both the results

# since the coroutines are scheduled and run immeadiately we dont see any concurrency benefits
