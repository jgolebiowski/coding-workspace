import math
import multiprocessing as mp
import sys
from datetime import datetime
import queue

TIMEOUT_LONG = 600
TIMEOUT_SHORT = 0.01


def paralll_worker(target_function,
                   task_queue,
                   result_queue,
                   fixed_args,
                   verbose=True):
    """
    Function to perform parallel work on a target_function and send the
    results back to the master process using Pipes.
    Each entry will be a tuple: (*target_function_input, target_function_output)

    Parameters
    ----------
    target_function : function
        Function to run, will be called as target_function(*(input + fixed_args))
    task_queue : multiprocessing.Queue
        Queue with partition names
    result_queue : multiprocessing.Queue
        Queue where IDs of partitions stored in plasma store are kept
    fixed_args : tuple
        Fixed args to pass to every function call
    verbose : bool
        If True, print logs to stderr
    """
    while (True):
        try:
            task = task_queue.get(block=True, timeout=TIMEOUT_SHORT)

            if verbose:
                print(datetime.now(), "This {} working on {}".format(mp.current_process(), task), file=sys.stderr)
                sys.stderr.flush()

            res = target_function(*(task + fixed_args))
            result_queue.put((*task, res))
        except queue.Empty:
            break


def parallel_control(target_function, list2process, fixed_args=None, num_threads=None, start_method="spawn", verbose=True):
    """Process a list in parallel by spawning only necessary number of processes

    Parameters
    ----------
    target_function : function
        Function to run, will be called as function(*(args +fixed_args))
    list2process : list[tuple]
        List with inputs to the target_function, if None an empty tuple is used
    fixed_args : tuple
        Fixed args ot pass to every function call, if None an empty tuple is used
    num_threads : int
        Number of threads ot use, if None multiprocessing.cpu_count() is used
    start_method : str
        Specify the start method, should be "spawn" or "fork"
    verbose : bool
        If True, print logs to stderr

    Returns
    -------
    list[tuple]
        List of results in the form:
        (*input, output)
    """
    if start_method not in ["spawn", "fork"]:
        raise ValueError("start_method should be spawn or fork not {}".format(start_method))
    ctx = mp.get_context(start_method)

    if num_threads is None:
        num_threads = int(ctx.cpu_count() / 2)
    num_threads = max(1, num_threads)

    if fixed_args is None:
        fixed_args = ()

    tasks_queue = ctx.Queue()
    results_queue = ctx.Queue()

    for task in list2process:
        tasks_queue.put(task)

    processes = []
    for rank in range(num_threads):
        p = ctx.Process(target=paralll_worker,
                        args=(target_function,
                              tasks_queue,
                              results_queue,
                              fixed_args),
                        kwargs=dict(verbose=verbose)
                        )
        p.start()
        processes.append(p)

    # Extract results
    results = []
    for task in list2process:
        res = results_queue.get(block=True, timeout=TIMEOUT_LONG)
        results.append(res)

    # Exit completed processes
    for p in processes:
        p.join()
        p.terminate()

    return results


def power(x, power):
    return x ** power


def cube(x):
    return x ** 3


def main():
    list2process = [(idx,) for idx in range(10)]
    results = parallel_control(cube, list2process)
    print(results)

    results = parallel_control(power, list2process, fixed_args=(3,))
    inputs = [item[0] for item in results]
    outputs = [item[1] for item in results]
    print(inputs, outputs)


if (__name__ == "__main__"):
    main()
