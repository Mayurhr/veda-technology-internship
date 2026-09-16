import asyncio
import time

async def io_task(task_id):
    await asyncio.sleep(1)
    return f"Task {task_id} completed"

async def main():
    start = time.perf_counter()
    results = await asyncio.gather(
        *(io_task(task_id) for task_id in range(1, 6))
    )
    print("AsyncIO Results:")
    for result in results:
        print(result)
    print(f"Execution time: {time.perf_counter() - start:.2f} seconds")
if __name__ == "__main__":
    asyncio.run(main())
