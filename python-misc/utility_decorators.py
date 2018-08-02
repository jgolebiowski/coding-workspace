"""Utilities for dumpin and storing models"""
import functools
import logging
import sys
import time

logger = logging.getLogger(__name__)


def debug_this(some_function):
    """
    Wrapper that launches a post mortem pdb debugger on errors in the function
    """

    @functools.wraps(some_function)
    def wrapper(*args, **kwargs):
        try:
            some_function(*args, **kwargs)
        except:
            import ipdb
            type, value, traceback = sys.exc_info()
            print(type, value, traceback)
            ipdb.post_mortem(traceback)

    return wrapper


def profile(some_function):
    """
    Wrapper that profiles the time spent in a function
    """

    @functools.wraps(some_function)
    def wrapper(*args, **kwargs):
        started_at = time.time()
        some_function(*args, **kwargs)
        logging.info("Function {} took {:.4e}s".format(some_function.__name__, time.time() - started_at))

    return wrapper

# --- When you use a decorator, you're replacing one function with another. In other words, if you have a decorator
#
# def logged(func):
#     def with_logging(*args, **kwargs):
#         print func.__name__ + " was called"
#         return func(*args, **kwargs)
#     return with_logging
#
# --- then when you say
#
# @logged
# def f(x):
#     """does some math"""
#     return x + x * x
#
# ---- it's exactly the same as saying
#
# def f(x):
#     """does some math"""
#     return x + x * x
# f = logged(f)