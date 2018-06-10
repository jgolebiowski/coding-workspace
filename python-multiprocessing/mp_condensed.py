import multiprocessing as mp
import math


def chunks(l, n):
    """Iterator to divide a list into chunks of size n

    Parameters
    ----------
    l : iterable
        list
    n : int
        Chunk size
    """
    n = max(1, n)
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i:i + n]


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


def worker_cube(rank, size,
                output_queue=None,
                numbers=None):
    """
    Function to calcuate the cube of a numbers in a givne list.
    For each number, put
    tuple (int, float, float)
        (rank, number, number_squared)
    Into the Queue

    Parameters
    ----------
    rank : int
        process number
    size : int
        total number of processes
    output_queue : mp.Queue
        Quete to store the results in
    number : list[float]
        Numbers to cube
    """
    print("This is process {} out of {} operating on {}".format(rank, size, numbers))
    for number in numbers:
        output_queue.put((rank, number, number ** 3))


def fast_process_parallel(list2process):
    num_threads = 3

    # Start the Queue, this could be also a list, dict or a shared array.
    mp_manager = mp.Manager()
    output_queue = mp_manager.Queue()

    processes = []
    for rank, batch in enumerate(batchify(list2process, num_threads)):
        p = mp.Process(target=worker_cube,
                       args=(rank, num_threads),
                       kwargs=dict(numbers=batch,
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
    print(results)


def worker_square(rank, size,
                  output_queue=None,
                  number=None):
    """
    Function to calcuate the square of a number, puts
    tuple (int, float)
        (rank, number, number_squared)
    Into the Queue

    Parameters
    ----------
    rank : int
        process number
    size : int
        total number of processes
    output_queue : mp.Queue
        Quete to store the results in
    number : float
        Number to square
    """
    id = mp.current_process().ident
    print("This is task {} running on process {}, one out of {}".format(rank, id, size))
    output_queue.put((rank, number, number ** 2))


def process_parallel(list2process):
    max_num_threads = 4

    # Start the Queue, this could be also a list, dict or a shared array.
    mp_manager = mp.Manager()
    output_queue = mp_manager.Queue()

    for mini_list in chunks(list2process, max_num_threads):
        num_threads = len(mini_list)
        # Setup a list of processes that we want to run
        processes = []
        for rank in range(num_threads):
            p = mp.Process(target=worker_square,
                           args=(rank, num_threads),
                           kwargs=dict(number=mini_list[rank],
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
    print(results)


def pool_parallel(list2process):
    num_threads = 3
    num_task = len(list2process)

    # Create a pool of workers
    globalPool = mp.Pool(processes=num_threads)

    # Start the Queue, this could be also a list, dict or a shared array.
    mp_manager = mp.Manager()
    output_queue = mp_manager.Queue()

    # Setup a list of processes that we want to run
    for rank in range(num_task):
        # Apply the function asyncronously

        globalPool.apply_async(func=worker_square,
                               args=(rank, num_threads,),
                               kwds=dict(number=list2process[rank],
                                         output_queue=output_queue)
                               )

    # Do not allow any more entries
    globalPool.close()
    # Join the processes
    globalPool.join()

    # Extract results
    results = []
    while (not output_queue.empty()):
        results.append(output_queue.get())
    print(results)


def main():
    list2process = list(range(10))
    pool_parallel(list2process)
    process_parallel(list2process)
    fast_process_parallel(list2process)


if (__name__ == "__main__"):
    main()
