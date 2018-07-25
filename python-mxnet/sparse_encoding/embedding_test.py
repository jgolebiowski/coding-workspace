"""This is the gluon tutorial"""
import mxnet as mx
from mxnet import autograd, gluon
import numpy as np
from mxnet import metric
import os


class BasicEmbeddingNetwork(mx.gluon.HybridBlock):
    """Basic MLP written with mxnet"""

    def __init__(self, input_dim, output_dim, weight_init=None, model_ctx=None, dtype="float32", **kwargs):
        if weight_init is None:
            self.weight_init = mx.init.Xavier()
        else:
            self.weight_init = weight_init
        super(BasicEmbeddingNetwork, self).__init__(**kwargs)
        self.ctx = model_ctx

        self.embedding = mx.gluon.nn.Embedding(input_dim=input_dim,
                                               output_dim=output_dim,
                                               dtype=dtype,
                                               weight_initializer=self.weight_init)

    def hybrid_forward(self, F, x):
        return self.embedding(x)



def main():
    model_ctx = mx.cpu(0)
    data_ctx = mx.cpu(0)
    input = 3
    output = 4
    model = BasicEmbeddingNetwork(input, output)
    model.collect_params().initialize(model.weight_init, ctx=model.ctx)

    test = mx.nd.zeros((1, 3, 2, 2))
    test[0, :, 0, 0] = mx.nd.array([1, 2, 1])
    test[0, :, 0, 1] = mx.nd.array([1, 0, 1])
    test[0, :, 1, 0] = mx.nd.array([0, 1, 1])
    test[0, :, 1, 1] = mx.nd.array([2, 1, 1])
    expanded = model(test)
    embedded = mx.nd.sum(expanded, axis=1).transpose(axes=(0, 3, 1, 2))

    print(test)
    print(test[0, :, 0, 1])
    print(test[0, :, 1, 0])
    print(expanded)
    print(embedded)
    print(embedded[0, :, 0, 1])
    print(embedded[0, :, 1, 0])
    import ipdb; ipdb.set_trace()




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
