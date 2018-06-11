import multiprocessing as mp
import math


def power(x, power):
    return x ** power

def cube(x):
    return x ** 3


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
        result = target_function(*input, *fixed_args)
        output_queue.put((input, result))


def parallel_control(target_function, list2process, fixed_args=None, num_threads=None):
    """Process a list in parallel by spawning only necessary number of processes
    Parameters
    ----------
    target_function : function
        Function to run, will be called as function(*args, *fixed_args)
    list2process : list[tuple]
        List with inputs to the target_function, if None an empty tuple is used
    fixed_args : tuple
        Fixed args ot pass to every function call
    num_threads : int
        Number of threads ot use, if None multiprocessing.cpu_count() is used
    Returns
    -------
    list[tuple]
        List of results in the form
        (inuput, output)
    """
    if num_threads is None:
        num_threads = mp.cpu_count()
    if fixed_args is None:
        fixed_args = ()

    # Start the Queue, this could be also a list, dict or a shared array.
    mp_manager = mp.Manager()
    output_queue = mp_manager.Queue()

    processes = []
    for rank, batch in enumerate(batchify(list2process, num_threads)):
        p = mp.Process(target=paralll_worker,
                       args=(rank, num_threads),
                       kwargs=dict(target_function=target_function,
                                   batch=batch,
                                   fixed_args=fixed_args,
                                   output_queue=output_queue)
                       )
        processes.append(p)

    # Run processes
    for p in processes:
        p.start()

    # Exit completed processes
    for p in processes:
        p.join()

    # Extract results
    results = []
    while (not output_queue.empty()):
        results.append(output_queue.get())

    return results


def main():
    list2process = [(idx,) for idx in range(10)]
    results = parallel_control(cube, list2process)
    print(results)

    results = parallel_control(power, list2process, fixed_args=(3, ))
    inputs = [item[0] for item in results]
    outputs = [item[1] for item in results]
    print(inputs, outputs)


if (__name__ == "__main__"):
    main()
