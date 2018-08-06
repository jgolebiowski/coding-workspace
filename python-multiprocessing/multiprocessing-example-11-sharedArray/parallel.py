import math
import multiprocessing as mp
import multiprocessing.sharedctypes
import sys
from datetime import datetime
import numpy as np
from typing import List, Tuple


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

class SharedArray(object):
    def __init__(self, shape: List[int]=None, dtype: str="float32", fromnumpy: np.array=None):
        if fromnumpy is not None:
            result = np.ctypeslib.as_ctypes(fromnumpy)
            self.array = multiprocessing.sharedctypes.Array(result._type_, result, lock=False)
            self.shape = fromnumpy.shape
            self.dtype = fromnumpy.dtype
        else:
            if dtype == "float32":
                self.array = mp.Array("f", int(np.prod(shape)), lock=False)
            elif dtype == "double":
                self.array = mp.Array("d", int(np.prod(shape)), lock=False)
            elif dtype == "int":
                self.array = mp.Array("i", int(np.prod(shape)), lock=False)
            else:
                raise ValueError("Only supports float32, double and int")
            self.dtype=dtype
            self.shape=shape

    def tonumpy(self):
        return np.ctypeslib.as_array(self.array, shape=self.shape).reshape(self.shape)

    @staticmethod
    def fromnumpy(array):
        result = np.ctypeslib.as_ctypes(array)
        array = mp.Array(result._type_, result, lock=False)


def operate(rank: int, x: SharedArray):
    x = x.tonumpy()
    print(x.shape)
    x[0, :, rank] = rank

def main():
    list2process = [(idx,) for idx in range(10)]
    x = np.random.uniform(0, 1, (1, 1, 10))
    array = SharedArray(fromnumpy=x)
    results = parallel_control(operate, list2process, fixed_args=(array,))
    print(array.tonumpy())
    outputs = [item[1] for item in results]


if (__name__ == "__main__"):
    main()
