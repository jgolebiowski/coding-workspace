"""This is the gluon tutorial"""
import mxnet as mx
CTX=mx.cpu(0)

def operations():
    a = mx.nd.random.uniform(-1, 1, (3, 4))
    b = mx.nd.random.uniform(-1, 1, (3, 4))
    print(a)
    print(b)
    print(a.shape, a.size, a.dtype)
    mx.nd.elemwise_add(a, b, out=a)
    print(a[0:2, :])
    c = mx.nd.reshape(a, shape=(4, 3))
    print(c)

def context():
    a = mx.nd.random.uniform(-1, 1, (3, 4), ctx=CTX)
    b = mx.nd.random.uniform(-1, 1, (4, 3), ctx=CTX)

    # Operations are only allowed if the variables live in the same context
    c = mx.nd.dot(a, b)

    # It is possible to copy over variables between contexts
    d = mx.nd.random.uniform(-1, 1, (3, 4), ctx=CTX)
    d = d.as_in_context(CTX)

    e = mx.nd.dot(d, b)
    print(e)

def main():
    # operations()
    context()



if (__name__ == "__main__"):
    main()