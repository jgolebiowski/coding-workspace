"""This is the gluon tutorial"""
import mxnet as mx
from mxnet import autograd, gluon
import numpy as np
from mxnet import metric
import os


class BasicCNN(mx.gluon.nn.HybridBlock):
    """My Basic CNN"""

    def __init__(self, n_hidden, n_output, kernel_shapes, channels, pooling_window, pooling_strides, context=None,
                 **kwargs):
        super(BasicCNN, self).__init__(**kwargs)
        if not len(kernel_shapes) == len(channels) == len(pooling_window) == len(pooling_strides) == 2:
            raise ValueError

        self.ctx = context
        with self.name_scope():
            self.activ_relu = mx.gluon.nn.Activation("relu")
            self.conv0 = mx.gluon.nn.Conv2D(channels=channels[0],
                                            kernel_size=kernel_shapes[0],
                                            strides=(1, 1),
                                            padding=(0, 0),
                                            layout="NCHW")
            self.batchnorm0 = gluon.nn.BatchNorm(axis=1, center=True, scale=True)
            self.pool0 = mx.gluon.nn.MaxPool2D(pool_size=pooling_window[0],
                                               strides=pooling_strides[0],
                                               padding=(0, 0),
                                               layout="NCHW")
            self.conv1 = mx.gluon.nn.Conv2D(channels=channels[1],
                                            kernel_size=kernel_shapes[1],
                                            strides=(1, 1),
                                            padding=(0, 0),
                                            in_channels=channels[0],
                                            layout="NCHW")
            self.batchnorm1 = gluon.nn.BatchNorm(axis=1, center=True, scale=True)
            self.pool1 = mx.gluon.nn.MaxPool2D(pool_size=pooling_window[1],
                                               strides=pooling_strides[1],
                                               padding=(0, 0),
                                               layout="NCHW")

            self.flatten = gluon.nn.Flatten()
            self.dense0 = mx.gluon.nn.Dense(n_hidden)
            self.batchnorm3 = gluon.nn.BatchNorm(axis=1, center=True, scale=True)
            self.dense1 = mx.gluon.nn.Dense(n_output)

    def hybrid_forward(self, F, x, **kwargs):
        """
        Run forward
        """
        x = self.conv0(x)
        x = self.batchnorm0(x)
        x = self.activ_relu(x)
        x = self.pool0(x)

        x = self.conv1(x)
        x = self.batchnorm1(x)
        x = self.activ_relu(x)
        x = self.pool1(x)

        x = self.flatten(x)
        x = self.dense0(x)
        x = self.batchnorm3(x)
        x = self.activ_relu(x)

        x = self.dense1(x)
        return x


def evaluate_performance(data_loader, model):
    """Evaluate the models performance"""
    acc = mx.metric.Accuracy()

    for idx, (data, label) in enumerate(data_loader):
        data = data.as_in_context(model.ctx)
        label = label.as_in_context(model.ctx)
        pred = model(data)
        pred = mx.nd.argmax(pred, axis=1)
        acc.update(label, pred)
    return acc.get()


def transform(data, label):
    return mx.nd.transpose(data.astype(np.float32), (2,0,1))/255, label.astype(np.float32)


def main():
    model_ctx = mx.cpu(0)
    data_ctx = mx.cpu(0)

    mnist_train = gluon.data.vision.CIFAR10(train=True, transform=transform)
    mnist_test = gluon.data.vision.CIFAR10(train=False, transform=transform)

    n_hidden = 512
    n_output = 10
    kernel_shapes = [(5, 5), (5, 5)]
    channels = [20, 50]
    pooling_window = [(2, 2), (2, 2)]
    pooling_strides = [(2, 2), (2, 2)]

    num_examples = len(mnist_train)
    batch_size = 16
    n_batches = num_examples / batch_size
    epochs = 10
    lr = 1e-3

    train_dataloader = mx.gluon.data.DataLoader(mnist_train, batch_size, shuffle=True)
    test_dataloader = mx.gluon.data.DataLoader(mnist_test, batch_size, shuffle=False)

    model = BasicCNN(n_hidden, n_output, kernel_shapes, channels, pooling_window, pooling_strides, context=model_ctx)
    model.collect_params().initialize(mx.init.Xavier(), ctx=model.ctx)
    model.hybridize()
    print(model)

    softmax_cross_entropy = gluon.loss.SoftmaxCrossEntropyLoss()
    trainer = gluon.Trainer(model.collect_params(),
                            "adam",
                            dict(learning_rate=lr))

    for e in range(epochs):
        cum_loss = 0
        for idx, (data, label) in enumerate(train_dataloader):
            data = data.as_in_context(model.ctx)
            label = label.as_in_context(model.ctx)
            with autograd.record(train_mode=True):
                output = model(data)
                loss = softmax_cross_entropy(output, label)
            loss.backward()
            trainer.step(batch_size)
            cum_loss += mx.nd.sum(loss).asscalar()
        print("Loss after {:3d}: {:.3e}".format(e, cum_loss / n_batches))

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
