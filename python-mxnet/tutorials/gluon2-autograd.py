"""This is the gluon tutorial"""
import mxnet as mx
from mxnet import autograd

CTX = mx.cpu(0)


def main():
    # We need to attach the gradient-storage
    a = mx.nd.random.uniform(-1, 1, (3, 4), ctx=CTX)
    a.attach_grad()

    # MXnet only builds a graph when told to
    with mx.autograd.record():
        b = a * 2
        c = b + 2

    c.backward()
    print(a.grad)


def graph_updates():
    # The head grdient can be passed to the function in line with the chain rulerino
    a = mx.nd.random.uniform(-1, 1, (3, 4), ctx=CTX)
    a.attach_grad()

    # Attaching gradient to a new variable makes it a new leaf
    # That means that the gradient is not propagated further through it
    with mx.autograd.record():
        b = a * 2
        b.attach_grad()
        c = b * 3 + 2

    mx.autograd.backward(c)

    print(b.grad)
    print(a.grad)

def head_gradient():
    # The head grdient can be passed to the function in line with the chain rulerino
    a = mx.nd.random.uniform(-1, 1, (3, 4), ctx=CTX)
    a.attach_grad()

    # The gradient can be passed as a function to be progagated down a graph
    with mx.autograd.record():
        b = a * 2
        c = b * 3 + 2

    head_gradient = mx.nd.random.uniform(-1, 1, (3, 4), ctx=CTX)
    mx.autograd.backward(c, head_grads=head_gradient)
    print(a.grad)


if (__name__ == "__main__"):
    head_gradient()
