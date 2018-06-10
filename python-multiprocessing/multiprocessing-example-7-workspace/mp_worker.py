"""This is the mp worker"""
import multiprocessing as mp


def worker_square_queue(rank, size,
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
