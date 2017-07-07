import numpy as np

"""Softmax."""

scores = np.array([[1, 3],
                   [2, 1],
                   [3, 0.2]])

# scores *= 0.1


def softmaxRow(x):
    """Compute softmax given a vector of values"""
    expVector = np.exp(x)
    return np.divide(expVector, np.sum(expVector))


def softmaxOld(x):
    """Compute softmax values for each sets of scores in x."""
    return np.apply_along_axis(softmaxRow, 0, x)


def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    expMat = np.exp(x)
    return np.divide(expMat, np.sum(expMat, 0))
    # return np.apply_along_axis(softmaxRow, 0, x)


print(softmax(scores))

# Plot softmax curves
import matplotlib.pyplot as plt
x = np.arange(-2.0, 6.0, 0.1)
scores = np.vstack([x, np.ones_like(x), 0.2 * np.ones_like(x)])

plt.plot(x, softmax(scores).T, linewidth=2)
# plt.show()
