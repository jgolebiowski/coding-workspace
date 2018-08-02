import multiprocessing
import queue

def worker(rank, size, tasks_queue=None, results_queue=None):
    while (True):
        try:
            task = tasks_queue.get(block=True, timeout=0.1)
            res = str(task) + "_processed"
            results_queue.put((task, res))
        except queue.Empty:
            print("Finished all tasks on proc {} out of {}".format(rank, size))
            break


def parallel_control(list2process):
    context = multiprocessing.get_context("spawn")
    max_threads = max(1, int(context.cpu_count() / 2))

    task_queue = context.Queue()
    result_queue = context.Queue()
    list2process = list2process

    for task in list2process:
        task_queue.put(task)

    proc = []
    for idx in range(max_threads):
        p = context.Process(target=worker,
                            args=(idx, max_threads),
                            kwargs=dict(tasks_queue=task_queue,
                                        results_queue=result_queue
                                        ))
        p.start()
        proc.append(p)

    results = []
    for elm in list2process:
        results.append(result_queue.get())

    # Make sure work is finished before garbage collection
    print(results)
    for p in proc:
        p.join()
        p.terminate()


if __name__ == '__main__':
    parallel_control([idx for idx in range(10)])
