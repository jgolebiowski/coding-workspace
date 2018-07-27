import functools
import math
import multiprocessing as mp
import subprocess
import sys
import time
from datetime import datetime

import numpy as np
import pyarrow
import pyarrow.plasma


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


def paralll_worker(rank, size,
                   target_function=None,
                   batch=None,
                   fixed_args=None,
                   sender=None):
    """
    Function to perform parallel work on a target_function and send the
    results back to the master process using Pipes.
    Each entry will be a tuple: (target_function_input, target_function_output)
    Parameters
    ----------
    rank : int
        process number
    size : int
        total number of processes
    target_function : function
        Function to run, will be called as target_function(*(input + fixed_args))
    batch : list[tuple]
        Inputs to the target_function in the form of tuples
    fixed_args : tuple
        Fixed args to pass to every function call
    sender : multiprocessing.connection.Connection
        Sending end of the Pipe to pass the results back to the main thread
    """
    for input in batch:
        print(datetime.now(), "This is process {} out of {} operating on {}".format(rank, size, input), file=sys.stderr)
        sys.stderr.flush()
        res = target_function(*(input + fixed_args))
        sender.send((input, res))

    # The job is finished, close the pipe
    sender.close()


def parallel_control(target_function, list2process, fixed_args=None, num_threads=None, start_method="spawn"):
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
        List of results in the form:
        ((inuput, ), output)
    """
    if start_method not in ["spawn", "fork"]:
        raise ValueError("start_method should be spawn or fork not {}".format(start_method))
    ctx = mp.get_context(start_method)

    if num_threads is None:
        num_threads = int(ctx.cpu_count() / 2)
    num_threads = min(num_threads, len(list2process))

    if fixed_args is None:
        fixed_args = ()

    processes = []
    receivers = []
    for rank, batch in enumerate(batchify(list2process, num_threads)):
        rcvr, sndr = ctx.Pipe(duplex=False)
        p = ctx.Process(target=paralll_worker,
                        args=(rank, num_threads),
                        kwargs=dict(target_function=target_function,
                                    batch=batch,
                                    fixed_args=fixed_args,
                                    sender=sndr)
                        )
        p.start()
        processes.append(p)
        receivers.append(rcvr)

        # Close the sender in the master thread. The only alive reference remains in
        # the worker threads. If master-version of the sender is not closed, the pipe
        # will remain alive even if workers close their end.
        sndr.close()

    # Extract results
    results = []
    while (len(receivers) > 0):
        current = receivers.pop(0)
        try:
            msg = current.recv()
            results.append(msg)
            receivers.append(current)
        except EOFError:
            pass

    # Exit completed processes
    for p in processes:
        p.join()
        p.terminate()

    return results


def profile(some_function):
    """
    Wrapper that profiles the time spent in a function
    """

    @functools.wraps(some_function)
    def wrapper(*args, **kwargs):
        started_at = time.time()
        some_function(*args, **kwargs)
        print("Function {} took {:.4e}s".format(some_function.__name__, time.time() - started_at))

    return wrapper


def classic(x, dims):
    return np.random.uniform(0, 1, (dims, dims)) * x


@profile
def main():
    nelemes = 10
    dims = int(3e3)
    list2process = [(idx,) for idx in range(nelemes)]
    results = parallel_control(classic, list2process, fixed_args=(dims,), start_method="fork")
    inputs = [item[0][0] for item in results]
    outputs = [item[1].shape for item in results]
    print(inputs)
    print(outputs)


def pyarrow_way(x, dims, plasma_dir):
    # Create the data
    data = np.random.uniform(0, 1, (dims, dims)) * x

    # Connect to plasma client and put the object
    client = pyarrow.plasma.connect(plasma_dir, "", 0)
    object_id = client.put(data)
    client.disconnect()

    return object_id


@profile
def main_pyarrow2(PLASMA_DIR):
    nelemes = 10
    dims = int(3e3)
    list2process = [(idx,) for idx in range(nelemes)]
    print("Starting")
    results = parallel_control(pyarrow_way, list2process,
                               fixed_args=(dims, PLASMA_DIR),
                               start_method="fork")
    inputs = [item[0][0] for item in results]
    outputs = [item[1] for item in results]

    # Connect to plasma client
    print("Connecting")
    client = pyarrow.plasma.connect(PLASMA_DIR, "", 0)

    # Get the arrow object by ObjectID.
    print("Get results")
    array_list = client.get(outputs, timeout_ms=0)
    if any([array is pyarrow.plasma.ObjectNotAvailable for array in array_list]):
        raise RuntimeError("Could not retrieve results. Probably run out of Plasma memory and not all objects could be stored")

    print([array.shape for array in array_list])
    print("Releasing data")
    for item_id in outputs:
        client.release(item_id)

    client.disconnect()
    print("FINISHED ITERATION")

def main_pyarrow(PLASMA_DIR):
    nelemes = 10
    dims = int(1e3)
    list2process = [(idx,) for idx in range(nelemes)]
    # Connect to plasma client
    print("Connecting")
    client = pyarrow.plasma.connect(PLASMA_DIR, "", 0)

    for i in range(10):
        print("Starting")
        results = parallel_control(pyarrow_way, list2process,
                                   fixed_args=(dims, PLASMA_DIR),
                                   start_method="fork")
        inputs = [item[0][0] for item in results]
        outputs = [item[1] for item in results]


        # Get the arrow object by ObjectID.
        print("Get results")
        array_list = client.get(outputs, timeout_ms=0)
        if any([array is pyarrow.plasma.ObjectNotAvailable for array in array_list]):
            raise RuntimeError("Could not retrieve results. Probably run out of Plasma memory and not all objects could be stored")

        print("FINISHED ITERATION")

if (__name__ == "__main__"):
    MEMORY_GB = 1 * 10 ** 9
    PLASMA_DIR = "/tmp/plasma"
    command = "plasma_store -m {} -s {}".format(MEMORY_GB, PLASMA_DIR)
    pid = subprocess.Popen(command.split())
    time.sleep(0.1)
    main_pyarrow2(PLASMA_DIR)
    main()
