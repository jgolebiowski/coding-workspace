"""Test script
This uses the line_profiler decorators to do the profiling and calling the report printing functionality at the end.
"""
import line_profiler
profile = line_profiler.LineProfiler()


@profile
def different_test():
    """Some function"""
    a = 1 + 2
    return True

@profile
def test_function(first: str, second: str="ending") -> str:
    """Print two messages
    Parameters
    ----------
    first : str
        Description
    second : str
        Description
    Returns
    -------
    str
        Description
    """
    different_test()
    result = "first message: {}, second message: {}".format(first, second)
    return result

@profile
def main():
    return test_function("elo", "melo")



if (__name__ == "__main__"):
    main()
    profile.print_stats()
