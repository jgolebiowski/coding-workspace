from line_profiler import LineProfiler


def profile_functions(task, functions=None, parameters=None):
    """Profile given functions with the provided task"""
    lp = LineProfiler()

    if functions is None:
        functions = []

    for fnc in functions:
        lp.add_function(fnc)

    lp_wrapper = lp(task)
    lp_wrapper(parameters)
    lp.print_stats()


def different_test():
    """Some function"""
    a = 1 + 2
    return True


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


def main():
    """Profile the function"""
    lp = LineProfiler()
    
    functions = [test_function, different_test]
    
    for fnc in functions:
        lp.add_function(fnc)

    lp_wrapper = lp(test_function)
    lp_wrapper("elo", second="melo")
    
    lp.print_stats()


if (__name__ == "__main__"):
    main()