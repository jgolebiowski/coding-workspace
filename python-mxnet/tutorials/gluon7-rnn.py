"""This is the gluon tutorial"""
import mxnet as mx
from mxnet import autograd, gluon
import numpy as np
from mxnet import metric
import os


class BasicGRU(mx.gluon.Block):
    """My basic implementation of a GRU with gluon"""

    def __init__(self, input_size, hidden_size, num_layers, dropout, context, **kwargs):
        super(BasicGRU, self).__init__(**kwargs)
        self.ctx = context
        with self.name_scope():
            self.activ = mx.gluon.nn.Activation("relu")
            self.rnn0 = mx.gluon.rnn.GRU(hidden_size=hidden_size,
                                         num_layers=num_layers,
                                         dropout=dropout,
                                         layout="TNC",
                                         input_size=input_size)
            self.dense0 = mx.gluon.nn.Dense(input_size,
                                            in_units=hidden_size,
                                            flatten=False)

    def forward(self, inputs, hidden, *args, **kwargs):
        output, hidden = self.rnn0(inputs, hidden)
        output = self.dense0(output)
        return output, hidden


def sample(prefix, num_chars, character_dict, vocab_size, character_list, model, num_hidden, ctx):
    #####################################
    # Initialize the string that we'll return to the supplied prefix
    #####################################
    string = prefix

    #####################################
    # Prepare the prefix as a sequence of one-hots for ingestion by RNN
    #####################################
    prefix_length = len(prefix)
    prefix_numerical = [character_dict[char] for char in prefix]
    input = one_hots(prefix_numerical, vocab_size, ctx).reshape((prefix_length, 1, -1))

    #####################################
    # Set the initial state of the hidden representation ($h_0$) to the zero vector
    #####################################
    sample_state = mx.nd.zeros(shape=(1, 1, num_hidden), ctx=ctx)

    #####################################
    # For num_chars iterations,
    #     1) feed in the current input
    #     2) sample next character from from output distribution
    #     3) add sampled character to the decoded string
    #     4) prepare the sampled character as a one_hot (to be the next input)
    #####################################
    for i in range(num_chars):
        outputs, sample_state = model(input, sample_state)
        pnd = mx.nd.softmax(outputs[-1][0])
        choice = np.random.choice(vocab_size, p=pnd.asnumpy())
        string += character_list[choice]
        input = one_hots([choice], vocab_size, ctx).reshape((1, 1, -1))
    return string


def one_hots(numerical_list, vocab_size, ctx):
    result = mx.nd.zeros((len(numerical_list), vocab_size), ctx=ctx)
    for i, idx in enumerate(numerical_list):
        result[i, idx] = 1.0
    return result


def textify(embedding, character_list):
    result = ""
    indices = mx.nd.argmax(embedding, axis=1).asnumpy()
    for idx in indices:
        result += character_list[int(idx)]
    return result


def prep_dataset(batch_size, ctx, num_samples, seq_length, time_machine_numerical, vocab_size):
    """Prepare dataset"""
    dataset = one_hots(time_machine_numerical[0:seq_length * num_samples], vocab_size, ctx)
    print("1", dataset.shape)
    dataset = dataset.reshape((num_samples, seq_length, vocab_size))
    print("2", dataset.shape)

    num_batches = len(dataset) // batch_size
    train_data = dataset[:num_batches * batch_size]
    print("3", train_data.shape)

    train_data = train_data.reshape((num_batches, batch_size, seq_length, vocab_size))
    # swap batch_size and seq_length axis to make later access easier
    print("4", train_data.shape)
    train_data = mx.nd.swapaxes(train_data, 1, 2)
    print("5", train_data.shape)

    labels = one_hots(time_machine_numerical[1:seq_length * num_samples + 1], vocab_size, ctx)
    train_labels = labels.reshape((num_batches, batch_size, seq_length, vocab_size))
    # swap batch_size and seq_length axis to make later access easier
    train_labels = mx.nd.swapaxes(train_labels, 1, 2)

    return train_data, train_labels, num_batches


def mx_detach(hidden):
    if isinstance(hidden, (tuple, list)):
        hidden = [i.detach() for i in hidden]
    else:
        hidden = hidden.detach()
    return hidden

def main():
    with open(os.path.join("data", "timemachine.txt"), "r") as fp:
        time_machine = fp.read().lower()

    time_machine = time_machine[:-38083]
    # time_machine = time_machine[0: 1000]

    character_list = list(set(time_machine))
    vocab_size = len(character_list)
    character_dict = {}
    for e, char in enumerate(character_list):
        character_dict[char] = e
    time_machine_numerical = [character_dict[char] for char in time_machine]

    batch_size = 16
    seq_length = 32
    num_samples = (len(time_machine_numerical) - 1) // seq_length
    ctx = mx.cpu(0)

    hidden_size = 512
    lr = 1e-3

    train_data, train_labels, num_batches = prep_dataset(batch_size, ctx, num_samples, seq_length,
                                                         time_machine_numerical, vocab_size)
    print(train_data.shape)

    model = BasicGRU(vocab_size, hidden_size, 1, 0.0, ctx)
    model.collect_params().initialize(mx.init.Xavier(), ctx=model.ctx)
    print(model)

    softmax_cross_entropy = gluon.loss.SoftmaxCrossEntropyLoss(sparse_label=False, batch_axis=1)
    trainer = gluon.Trainer(model.collect_params(),
                            "adam",
                            dict(learning_rate=lr))

    epochs = 3
    for e in range(epochs):
        cum_loss = 0.
        state = mx.nd.zeros(shape=(1, batch_size, hidden_size), ctx=ctx)

        for i in range(num_batches):
            data_one_hot = train_data[i]
            label_one_hot = train_labels[i]
            state = mx_detach(state)
            with autograd.record():
                outputs, state = model(data_one_hot, state)
                loss = softmax_cross_entropy(outputs, label_one_hot)
            mx.autograd.backward(loss)

            trainer.step(batch_size)
            cum_loss += mx.nd.sum(loss)

        print("------ Loss after {:3d}: {}".format(e, cum_loss / num_batches))
        print(sample("the time ma", 1024, character_dict, vocab_size, character_list, model, hidden_size, ctx))
        print(sample("the medical man rose, came to the lamp", 1024, character_dict, vocab_size, character_list, model, hidden_size, ctx))
    # print(sample("the project", 1000, character_dict, vocab_size, character_list, model, hidden_size, ctx))


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
