"""Test script
This uses the line_profiler decorators to do the profiling
This requires:
    installation of line_profiler
    kernprof script in the bin (should be automatic)

run by: kernprof -l -v profile_decorators.py

The binary results are stored in: profile_decorators.py.lprof and can be viewed by:
python -m line_profiler profile_decorators.py.lprof
"""

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
