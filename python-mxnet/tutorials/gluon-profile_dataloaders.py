"""This is the gluon tutorial"""
import mxnet as mx
from mxnet import autograd, gluon
import numpy as np

DATA_CTX = mx.cpu(0)
MODEL_CTX = mx.cpu(0)

def linear_function(x, a0=2, a1=3, c=4):
    return x[0] * a0 + x[1] * a1 + c

def linear_function2(x, a0=2, a1=3, c=4):
    return x[:, 0] * a0 + x[:, 1] * a1 + c

def main():
    num_inputs = 2
    num_outputs = 1
    num_examples = 10000
    batch_size=5

    x_train = [np.random.uniform(size=(num_inputs)) for idx in range(num_examples)]
    y_train = [linear_function(x_train[idx]) + np.random.uniform() * 0.1 for idx in range(num_examples)]
    train_dataset = mx.gluon.data.ArrayDataset(x_train, y_train)
    train_dataloader = mx.gluon.data.DataLoader(dataset=train_dataset,
                                                batch_size=batch_size,
                                                shuffle=True)
    for idx, (data, label) in enumerate(train_dataloader):
        d = data
        l = label

    x_train2 = mx.nd.random.uniform(shape=(num_examples, num_inputs), ctx=DATA_CTX)
    noise2 = mx.nd.random.uniform(shape=(num_examples, ), ctx=DATA_CTX) * 0.1
    y_train2 = linear_function2(x_train2) + noise2
    train_dataset2 = mx.gluon.data.ArrayDataset(x_train2, y_train2)
    train_dataloader2 = mx.gluon.data.DataLoader(dataset=train_dataset2,
                                                batch_size=batch_size,
                                                shuffle=True)
    for idx, (data, label) in enumerate(train_dataloader2):
        d = data
        l = label

    x_train3 = [mx.nd.random.uniform(shape=(num_inputs), ctx=DATA_CTX) for idx in range(num_examples)]
    y_train3 = [linear_function(x_train3[idx]) + mx.nd.random.uniform(ctx=DATA_CTX) * 0.1 for idx in range(num_examples)]
    train_dataset3 = mx.gluon.data.ArrayDataset(x_train3, y_train3)
    train_dataloader3 = mx.gluon.data.DataLoader(dataset=train_dataset3,
                                                batch_size=batch_size,
                                                shuffle=True)
    for idx, (data, label) in enumerate(train_dataloader3):
        d = data
        l = label

    x_train4 = np.random.uniform(size=(num_examples, num_inputs))
    noise4 = np.random.uniform(size=(num_examples, )) * 0.1
    y_train4 = linear_function2(x_train4) + noise4
    train_dataset4 = mx.gluon.data.ArrayDataset(x_train4, y_train4)
    train_dataloader4 = mx.gluon.data.DataLoader(dataset=train_dataset4,
                                                batch_size=batch_size,
                                                shuffle=True)
    for idx, (data, label) in enumerate(train_dataloader4):
        d = data
        l = label


def profile_main():
    """Profile the function"""
    from line_profiler import LineProfiler
    lp = LineProfiler()

    functions = [main]

    for fnc in functions:
        lp.add_function(fnc)

    lp_wrapper = lp(main)
    result = lp_wrapper()
    lp.print_stats()

if (__name__ == "__main__"):
    profile_main()