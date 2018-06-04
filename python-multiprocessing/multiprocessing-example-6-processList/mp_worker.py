"""This is the mp worker"""


def worker_square(rank, size,
                  number=None):
    """
    Function to calcuate the square of a number

    Parameters
    ----------
    rank : int
        process number
    size : int
        total number of processes
    number : float
        Number to square

    Returns
    -------
    tuple (int, float)
        returns (rank, number_squared)
    """
    print("This is process {} out of {}".format(rank, size))
    return (rank, number ** 2)

def worker_square_list(rank, size,
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
    print("This is process {} out of {}".format(rank, size))
    output_queue.put((rank, number, number ** 2))