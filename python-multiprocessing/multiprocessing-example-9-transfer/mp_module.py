import multiprocessing as mp
import math
import numpy as np
import gc
from datetime import datetime



def make_array(x, size):
    return np.random.uniform(0, 1, (size, size, size))


def batchify(l, n):
    """
    Iterator to divide a list into n chunks,
    All but the last are equal size
    Parameters
    ----------
    l : iterable
        list
    n : int
        Number of chunks
    """
    n = min(len(l), n)
    n = max(1, n)
    chunksize = int(math.ceil(len(l) / n))

    for i in range(0, len(l), chunksize):
        # Create an index range for l of chunksize items:
        yield l[i:i + chunksize]


def paralll_worker(rank, size,
                   target_function=None,
                   batch=None,
                   fixed_args=None,
                   output_queue=None):
    """
    Function to perform parallel work on a target_function and dump the results
    into the output queue, each entry will be structured as
    (target_function_input, target_function_output)
    Parameters
    ----------
    rank : int
        process number
    size : int
        total number of processes
    target_function : function
        Function to run, will be called as function(*args, *fixed_args)
    batch : list[tuple]
        Inputs to the target_function in the form of tuples
    fixed_args : tuple
        Fixed args ot pass to every function call
    output_queue : mp.Queue
        Quete to store the results in
    """
    for input in batch:
        print(datetime.now(), "This is process {} out of {} operating on {}".format(rank, size, input))
        result = target_function(*input, *fixed_args)
        output_queue.put((input, result))


def parallel_control(target_function, list2process, fixed_args=None, num_threads=None, start_method="fork"):
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

    Returns
    -------
    list[tuple]
        List of results in the form
        (inuput, output)
    """
    if start_method not in ["spawn", "fork"]:
        raise ValueError("start_method should be spawn or fork not {}".format(start_method))
    ctx = mp.get_context(start_method)

    if num_threads is None:
        num_threads = ctx.cpu_count()
    num_threads = min(num_threads, len(list2process))

    if fixed_args is None:
        fixed_args = ()

    # Start the Queue, this could be also a list, dict or a shared array.
    mp_manager = ctx.Manager()
    output_queue = mp_manager.Queue()

    processes = []
    print(datetime.now(), "Starting processes")
    for rank, batch in enumerate(batchify(list2process, num_threads)):
        p = ctx.Process(target=paralll_worker,
                        args=(rank, num_threads),
                        kwargs=dict(target_function=target_function,
                                    batch=batch,
                                    fixed_args=fixed_args,
                                    output_queue=output_queue)
                        )
        p.start()
        processes.append(p)

    print(datetime.now(), "Joining processes")
    # Join processes, wait for completion
    for p in processes:
        p.join()

    # Extract results
    print(datetime.now(), "Extracting results from processes")
    results = []
    while (not output_queue.empty()):
        results.append(output_queue.get())

    # Exit completed processes
    print(datetime.now(), "Terminating processes")
    for p in processes:
        p.terminate()

    print(datetime.now(), "Finished")
    return results


def main():
    list2process = [(None, ) for idx in range(4)]
    results = parallel_control(make_array, list2process, fixed_args=(200, ), num_threads=2)
    inputs = [item[0][0] for item in results]
    outputs = [item[1] for item in results]


if (__name__ == "__main__"):
    main()
