import multiprocessing as mp
from mp_module import parallel_control
import numpy as np
import ctypes

def generate_array(idx, arry, array_properties):
    np_arry = mpArray2numpy(arry, array_properties)
    np_arry[1, 2] = idx


def mpArray2numpy(arry, array_properties):
    """
    Convert a multiprocessing array to numpy
    """
    return np.frombuffer(arry.get_obj(),
                         dtype=array_properties["dtype"]).reshape(array_properties["shape"])
def main():
    shape = (5, 5)
    array_properties = dict(shape=shape,
                            size=shape[0] * shape[1],
                            dtype=ctypes.c_float)

    list2process = [None for i in range(10)]
    output_list = [None for i in range(10)]
    for idx in range(len(list2process)):
        mp_arry = mp.Array(array_properties["dtype"], array_properties["size"])
        list2process[idx] = (idx, mp_arry)
        output_list[idx] = mpArray2numpy(mp_arry, array_properties)

    parallel_control(generate_array, list2process, fixed_args=(array_properties, ), return_results=False)
    for element in output_list:
        print(element)


if (__name__ == "__main__"):
    main()
