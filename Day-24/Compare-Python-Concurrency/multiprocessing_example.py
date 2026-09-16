import time
from multiprocessing import Process, Queue
def cpu_task(task_id, queue):
    total = 0
    for number in range(1, 1000000):
        total += number * number
    queue.put(f"Task {task_id} completed")
if __name__ == "__main__":
    start = time.perf_counter()
    queue = Queue()
    processes = []
    for task_id in range(1, 5):
        process = Process(target=cpu_task, args=(task_id, queue))
        processes.append(process)
        process.start()
    for process in processes:
        process.join()
    print("Multiprocessing Results:")
    while not queue.empty():
        print(queue.get())
    print(f"Execution time: {time.perf_counter() - start:.2f} seconds")
