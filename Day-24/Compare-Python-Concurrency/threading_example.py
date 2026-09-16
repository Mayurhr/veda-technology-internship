import time
import threading
def io_task(task_id):
    time.sleep(1)
    return f"Task {task_id} completed"
start = time.perf_counter()
threads = []
results = []
def worker(task_id):
    results.append(io_task(task_id))
for task_id in range(1, 6):
    thread = threading.Thread(target=worker, args=(task_id,))
    threads.append(thread)
    thread.start()
for thread in threads:
    thread.join()
print("Threading Results:")
for result in results:
    print(result)
print(f"Execution time: {time.perf_counter() - start:.2f} seconds")
