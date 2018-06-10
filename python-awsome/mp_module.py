import multiprocessing as mp
import math


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
        Function to run
    batch : list[tuple]
        Inputs to the target_function in the form of tuples
    output_queue : mp.Queue
        Quete to store the results in
    """
    print("This is process {} out of {} operating on {}".format(rank, size, batch))
    for input in batch:
        result = target_function(*input)
        output_queue.put((input, result))


def parallel_control(target_function, list2process, num_threads):
    """Process a list in parallel by spawning only necessary number of processes

    Parameters
    ----------
    target_function : function
        Function to parallelise
    list2process : list[tuple]
        List with inputs to the target_function
    num_threads : int
        Number of threads ot use

    Returns
    -------
    list[tuple]
        List of results in the form
        (inuput, output)
    """

    # Start the Queue, this could be also a list, dict or a shared array.
    mp_manager = mp.Manager()
    output_queue = mp_manager.Queue()

    processes = []
    for rank, batch in enumerate(batchify(list2process, num_threads)):
        p = mp.Process(target=paralll_worker,
                       args=(rank, num_threads),
                       kwargs=dict(target_function=target_function,
                                   batch=batch,
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
    print(parallel_control(cube, list2process, 3))


if (__name__ == "__main__"):
    main()
