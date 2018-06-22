import multiprocessing as mp
import math
import numpy as np
from datetime import datetime



def make_array(x, size):
    return np.random.uniform(0, 1, (size, size, size))
    # return x


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
    results = []
    for input in batch:
        print(datetime.now(), "This is process {} out of {} operating on {}".format(rank, size, input))
        res = target_function(*input, *fixed_args)
        results.append(res)

    print(datetime.now(), "Pushing to pipe")
    output_queue.put((batch, results))


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
        inouts in an arbitary order
    list
        results in the same order as inputs
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
    inputs = []
    while (not output_queue.empty()):
        res = output_queue.get()
        inputs.extend(res[0])
        results.extend(res[1])

    # Exit completed processes
    print(datetime.now(), "Terminating processes")
    for p in processes:
        p.terminate()

    print(datetime.now(), "Finished")
    return inputs, results


def main():
    list2process = [(idx, ) for idx in range(4)]
    inputs, results = parallel_control(make_array, list2process, fixed_args=(175, ), num_threads=2)
    # print(inputs)
    # print(results)


if (__name__ == "__main__"):
    main()
