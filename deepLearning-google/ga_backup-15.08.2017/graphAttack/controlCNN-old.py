import graphAttack as ga
import numpy as np
import pickle
import tensorflow as tf
"""Control script"""

np.random.seed(231)
x = np.random.randn(3, 2, 8, 8)
dout = np.random.randn(3, 2, 4, 4)
pool_param = {'pool_height': 2, 'pool_width': 2, 'stride': 2}

out, cache = ga.max_pool_forward_im2col(x, pool_param)
dx = ga.max_pool_backward_im2col(dout, cache)


feed = ga.Variable(x)
maxPoolOp = ga.MaxPoolOperation(inputA=feed, poolHeight=2, poolWidth=2, stride=2)
print("Forward pass")
print(maxPoolOp.getValue())
print(maxPoolOp.getValue() - out)

gaGradient = maxPoolOp.performGradient(input=0, out=dout)
print("Backwards pass")
print(gaGradient)
print(gaGradient - dx)




# x_shape = (2, 3, 4, 4)
# x = np.linspace(-0.3, 0.4, num=np.prod(x_shape)).reshape(x_shape)
# pool_param = {'pool_width': 2, 'pool_height': 2, 'stride': 2}

# out, _ = ga.max_pool_forward_im2col(x, pool_param)

# correct_out = np.array([[[[-0.26315789, -0.24842105],
#                           [-0.20421053, -0.18947368]],
#                          [[-0.14526316, -0.13052632],
#                           [-0.08631579, -0.07157895]],
#                          [[-0.02736842, -0.01263158],
#                           [ 0.03157895,  0.04631579]]],
#                         [[[ 0.09052632,  0.10526316],
#                           [ 0.14947368,  0.16421053]],
#                          [[ 0.20842105,  0.22315789],
#                           [ 0.26736842,  0.28210526]],
#                          [[ 0.32631579,  0.34105263],
#                           [ 0.38526316,  0.4       ]]]])

# feed = ga.Variable(x)
# maxPoolOp = ga.MaxPoolOperation(inputA=feed, poolHeight=2, poolWidth=2, stride=2)

# print(maxPoolOp.getValue() - out)

