"""This is the gluon tutorial"""
import mxnet as mx
from mxnet import autograd, gluon
import numpy as np

DATA_CTX = mx.cpu(0)
MODEL_CTX = mx.cpu(0)


def linear_function2(x, a0=2, a1=3, c=4):
    return x[:, 0] * a0 + x[:, 1] * a1 + c


def main():
    num_inputs = 2
    num_outputs = 1
    num_examples = 10000
    batch_size = 5
    n_batches = num_examples / batch_size
    epochs = 10
    lr = 1e-3


    x_train = mx.nd.random.uniform(shape=(num_examples, num_inputs), ctx=DATA_CTX)
    noise = mx.nd.random.uniform(shape=(num_examples, ), ctx=DATA_CTX) * 0.1
    y_train = linear_function2(x_train) + noise
    train_dataset = mx.gluon.data.ArrayDataset(x_train, y_train.reshape((-1, 1)))
    train_dataloader = mx.gluon.data.DataLoader(dataset=train_dataset,
                                                batch_size=batch_size,
                                                shuffle=True)

    model = mx.gluon.nn.Dense(num_outputs, in_units=num_inputs)
    model.collect_params().initialize(init=mx.init.Normal(1),
                                      ctx=MODEL_CTX)
    loss_func = gluon.loss.L2Loss()
    optimizer = gluon.Trainer(model.collect_params(),
                              "adam",
                              optimizer_params=dict(learning_rate=lr))
    print(model)

    for e in range(epochs):
        cumulative_loss = 0
        for idx, (data, label) in enumerate(train_dataloader):
            data = data.as_in_context(MODEL_CTX)
            label = label.as_in_context(MODEL_CTX)

            with mx.autograd.record():
                yhat = model(data)
                loss = loss_func(yhat, label)
            mx.autograd.backward(loss)
            optimizer.step(batch_size)
            cumulative_loss += mx.nd.mean(loss).asscalar()
        print("Loss after {:3d}: {:.3e}".format(e, cumulative_loss / n_batches))

    print(model.weight.data())
    print(model.bias.data())





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
    return result

if (__name__ == "__main__"):
    main()