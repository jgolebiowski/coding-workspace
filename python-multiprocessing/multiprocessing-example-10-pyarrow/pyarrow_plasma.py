import gc
import subprocess
import time

import numpy as np
import pandas as pd
import pyarrow
import pyarrow.plasma
import scipy.sparse

def pyarrow_way(x, dims):
    # Create the data
    data = np.ones((dims, dims))
    # df = pd.DataFrame(data)
    # table = pyarrow.Table.from_pandas(df)
    # df_new = table.to_pandas()
    # data_new = df_new.values


    tensor = pyarrow.Tensor.from_numpy(data)

    # Connect to plasma client
    client = pyarrow.plasma.connect("/tmp/plasma", "", 0)

    # Create the object in Plasma
    object_id = pyarrow.plasma.ObjectID(np.random.bytes(20))
    data_size = pyarrow.get_tensor_size(tensor)
    buf = client.create(object_id, data_size)

    # Write the tensor into the Plasma-allocated buffer
    stream = pyarrow.FixedSizeBufferWriter(buf)
    pyarrow.write_tensor(tensor, stream)

    # Seal the Plasma object
    client.seal(object_id)
    client.disconnect()

    return object_id

def main():
    nelemes = 10
    dims = int(1e3)
    result = pyarrow_way(nelemes, dims)

    # Connect to plasma client
    client = pyarrow.plasma.connect("/tmp/plasma", "", 0)

    # Get the arrow object by ObjectID.
    [buffer] = client.get_buffers([result])

    # Reconstruct the Arrow tensor object.
    reader = pyarrow.BufferReader(buffer)
    tensor = pyarrow.read_tensor(reader)

    # Convert back to numpy
    array = tensor.to_numpy()
    print(array.shape)

def pyarrow_easy(x, dims):
    # Create the data
    data = dict(data=np.ones((dims, dims)),
                labels=[1, 2, 3])

    # Connect to plasma client
    client = pyarrow.plasma.connect("/tmp/plasma", "", 0)
    # Create the object in Plasma
    object_id = client.put(data)
    client.disconnect()

    return object_id

def main_easy():
    nelemes = 10
    dims = int(1e3)
    result = pyarrow_easy(nelemes, dims)

    # Connect to plasma client
    client = pyarrow.plasma.connect("/tmp/plasma", "", 0)

    # Get the arrow object by ObjectID.
    array = client.get(result)

    print(array["data"].shape)

    client.release(result)
    client.disconnect()
    print("Released")



if (__name__ == "__main__"):
    command = "plasma_store -m {} -s {}".format(10**9, "/tmp/plasma")
    pid = subprocess.Popen(command.split())
    time.sleep(0.1)
    main_easy()
