import time

def timeit(method):
    """

    Decorator to print execution time to screen.
    Usage:

    @timeit
    def func():
        pass
    """
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print("{:-<30}> {:.3e} s".format(method.__name__, (te - ts)))
        return result
    return timed