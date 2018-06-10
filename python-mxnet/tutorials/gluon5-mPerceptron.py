"""This is the gluon tutorial"""
import mxnet as mx
from mxnet import autograd, gluon
import numpy as np
from mxnet import metric
import os


class BasicDenseNetwork(mx.gluon.HybridBlock):
    """Basic MLP written with mxnet"""

    def __init__(self, n_input=None, n_hidden=None, n_output=None, droprate=0.5, model_ctx=None, **kwargs):
        super(BasicDenseNetwork, self).__init__(**kwargs)
        self.ctx = model_ctx
        with self.name_scope():
            self.drop0 = mx.gluon.nn.Dropout(droprate / 2)
            self.dense0 = mx.gluon.nn.Dense(n_hidden, in_units=n_input)
            self.drop1 = mx.gluon.nn.Dropout(droprate)
            self.dense1 = mx.gluon.nn.Dense(n_hidden, in_units=n_hidden)
            self.drop2 = mx.gluon.nn.Dropout(droprate)
            self.dense2 = mx.gluon.nn.Dense(n_output, in_units=n_hidden)

    def hybrid_forward(self, F, x):
        """Run forward"""
        x = self.drop0(x)
        x = F.relu(self.dense0(x))

        x = self.drop1(x)
        x = F.relu(self.dense1(x))

        x = self.drop2(x)
        x = self.dense2(x)
        return x


def evaluate_performance(data_loader, model):
    """Evaluate the models performance"""
    acc = mx.metric.Accuracy()

    for idx, (data, label) in enumerate(data_loader):
        data = data.as_in_context(model.ctx).reshape((-1, 784))
        label = label.as_in_context(model.ctx)
        pred = model(data)
        pred = mx.nd.argmax(pred, axis=1)
        acc.update(preds=pred, labels=label)
    return acc.get()


def transform(data, label):
    return data.astype(np.float32) / 255, label.astype(np.float32)


def main():
    model_ctx = mx.cpu(0)
    data_ctx = mx.cpu(0)

    mnist_train = gluon.data.vision.MNIST(train=True, transform=transform)
    mnist_test = gluon.data.vision.MNIST(train=False, transform=transform)

    num_inputs = mnist_train[0][0].size
    num_hidden = 256
    num_outputs = 10

    num_examples = len(mnist_train)
    batch_size = 64
    n_batches = num_examples / batch_size
    epochs = 2
    lr = 1e-3

    train_dataloader = mx.gluon.data.DataLoader(mnist_train, batch_size, shuffle=True)
    test_dataloader = mx.gluon.data.DataLoader(mnist_test, batch_size, shuffle=False)

    model = BasicDenseNetwork(n_input=num_inputs,
                              n_hidden=num_hidden,
                              n_output=num_outputs,
                              droprate=0.2,
                              model_ctx=model_ctx)
    model.collect_params().initialize(mx.init.Normal(0.01), ctx=model.ctx)
    softmax_cross_entropy = mx.gluon.loss.SoftmaxCrossEntropyLoss()
    trainer = mx.gluon.Trainer(model.collect_params(),
                               "adam",
                               dict(learning_rate=1e-3))
    model.hybridize()
    checkdir = "checkpoints"
    print(model)

    for e in range(epochs):
        cumulative_loss = 0
        for i, (data, label) in enumerate(train_dataloader):
            data = data.as_in_context(model_ctx).reshape((-1, 784))
            label = label.as_in_context(model_ctx)

            # Setting training mode ot true, this will enable dropout
            with autograd.record(train_mode=True):
                output = model(data)
                loss = softmax_cross_entropy(output, label)
            loss.backward()
            trainer.step(batch_size)
            cumulative_loss += mx.nd.sum(loss).asscalar()
        print("Loss after {:3d}: {:.3e}".format(e, cumulative_loss / n_batches))
        checkfile = os.path.join(checkdir, "checkpoint_{}.params".format(e))
        model.save_params(checkfile)

    # model.load_params(os.path.join(checkdir, "checkpoint_1.params"), model.ctx)
    print(evaluate_performance(test_dataloader, model))


def profile_main():
    """Profile the function"""
    from line_profiler import LineProfiler
    from mxnet.gluon.data.dataloader import default_batchify_fn
    from mxnet.gluon.data.sampler import BatchSampler

    lp = LineProfiler()

    functions = [main, mx.gluon.data.DataLoader.__iter__, default_batchify_fn, BatchSampler.__iter__, transform]

    for fnc in functions:
        lp.add_function(fnc)

    lp_wrapper = lp(main)
    result = lp_wrapper()
    lp.print_stats()
    return result


if (__name__ == "__main__"):
    main()
