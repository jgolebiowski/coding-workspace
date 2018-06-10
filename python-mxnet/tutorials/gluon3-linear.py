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

class LinearModel(object):
    """Simple linear model"""
    def __init__(self, n_input, n_output):
        self.w = mx.nd.random.uniform(shape=(n_input, n_output), ctx=MODEL_CTX)
        self.b = mx.nd.random.uniform(shape=(1, n_output), ctx=MODEL_CTX)

        self.params = (self.w, self.b)
        for p in self.params:
            p.attach_grad()

    def predict(self, x):
        """Propagate forward"""
        return mx.nd.dot(x, self.w) + self.b

def square_loss(yhat, y):
    """Standard square loss"""
    return mx.nd.mean(mx.nd.square(yhat - y))


class SGD(object):
    """Simple class for the SGD"""
    def __init__(self, model, lr=1e-3):
        self.model = model
        self.lr = lr

    def step(self):
        """Update the parameters"""
        for p in self.model.params:
            p -= self.lr * p.grad



def main():
    num_inputs = 2
    num_outputs = 1
    num_examples = 1000
    batch_size = 5
    n_batches = num_examples / batch_size
    epochs = 10
    lr = 1e-2


    x_train = [mx.nd.random.uniform(shape=(num_inputs), ctx=DATA_CTX) for idx in range(num_examples)]
    y_train = [linear_function(x_train[idx]) + mx.nd.random.uniform(ctx=DATA_CTX) * 0.1 for idx in range(num_examples)]
    train_dataset = mx.gluon.data.ArrayDataset(x_train, y_train)
    train_dataloader = mx.gluon.data.DataLoader(dataset=train_dataset,
                                                batch_size=batch_size,
                                                shuffle=True)

    # x_train = mx.nd.random.uniform(shape=(num_examples, num_inputs), ctx=DATA_CTX)
    # noise = mx.nd.random.uniform(shape=(num_examples, ), ctx=DATA_CTX) * 0.1
    # y_train = linear_function2(x_train) + noise
    # train_dataset = mx.gluon.data.ArrayDataset(x_train, y_train.reshape((-1, 1)))
    # train_dataloader = mx.gluon.data.DataLoader(dataset=train_dataset,
    #                                             batch_size=batch_size,
    #                                             shuffle=True)

    model = LinearModel(num_inputs, num_outputs)
    optimizer = SGD(model, lr)
    for e in range(epochs):
        cumulative_loss = 0
        for idx, (data, label) in enumerate(train_dataloader):
            data = data.as_in_context(MODEL_CTX)
            label = label.as_in_context(MODEL_CTX)

            with mx.autograd.record():
                out = model.predict(data)
                loss = square_loss(out, label)

            mx.autograd.backward(loss)
            optimizer.step()
            cumulative_loss += loss.asscalar()
        print(cumulative_loss / n_batches)

    print("Estimated params")
    print(model.w)
    print(model.b)




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
    profile_main()