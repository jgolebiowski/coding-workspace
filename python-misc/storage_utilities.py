"""Utilities for dumpin and storing models"""
import pickle
import os
import sys


MAX_BYTES = 2**31 - 1


def save_pickle_object(obj, filepath):
    """
    This is a defensive way to write pickle.write, allowing for very large files on all platforms

    Parameters
    ----------
    models : dict[name: model]
        A dictionary of models to use to create semnatic similarity columns
    path : str
        Path to the file to which models shuld be dumped
    """
    bytes_out = pickle.dumps(obj)
    n_bytes = sys.getsizeof(bytes_out)
    with open(filepath, 'wb') as f_out:
        for idx in range(0, n_bytes, MAX_BYTES):
            f_out.write(bytes_out[idx:idx+MAX_BYTES])


def load_pickle_object(filepath):
    """
    This is a defensive way to write pickle.load, allowing for very large files on all platforms

    Parameters
    ----------
    path : str
        Path to the file to which models shuld be dumped

    Returns
    -------
    object
        The objest loaded from the path or None if loading fails
    """

    try:
        input_size = os.path.getsize(filepath)
        bytes_in = bytearray(0)
        with open(filepath, 'rb') as f_in:
            for _ in range(0, input_size, MAX_BYTES):
                bytes_in += f_in.read(MAX_BYTES)
        obj = pickle.loads(bytes_in)
    except:
        return None
    return obj


def create_directory(experiment_dir, name):
    """
    Create a directory

    Parameters
    ----------
    experiment_dir : str
        Path to the experiemnt directory on the cluster
    name : str
        Directory name

    Returns
    -------
    str
        Path to the newly created direcotry
    """
    new_directory = os.path.join(experiment_dir, name)
    try:
        os.mkdir(new_directory)
    except OSError:
        pass
    return new_directory
