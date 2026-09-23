import asyncio
import time


def sync_fun(test_param: str)->str:
    print("This is a synchronous function")
    time.sleep(1)
    return f"Sync Result: {test_param}"
    
# also known as a co routine function
async def async_fun(test_param: str)-> str:
    print("This is an async function")
    await asyncio.sleep(1)
    return f"Async Result: {test_param}"

# Main is a co routine here
async def main():
    sync_res = sync_fun("Test")
    print(sync_res)


    # Working with Futures
    loop = asyncio.get_running_loop()
    future = loop.create_future()
    print(f"Empty Future: {future}")

    future.set_result("Future Result: Test")
    future_result = await future
    print(future_result)

    # Co routines 
    # Running the co routine funciton gave us a co routine object 
    # Coroutine Obj     Co routine function 
    coroutine_obj = async_fun("Test ")
    # this creates a co routine object but the funciton isnt executed
    print(coroutine_obj)

    # To run the co routine object and get the result we have to await it
    # When we run a co routine object like this directly its both scheduled on the event loop and run to completion at the same time
    coroutine_result = await coroutine_obj
    print(coroutine_result)

    task = asyncio.create_task(async_fun("Test"))
    print(task)

    task_result = await task
    print(task_result)




# To run async funcitons we need to start an event loop

if __name__ == "__main__":
    # this starts an event loop
    asyncio.run(main())