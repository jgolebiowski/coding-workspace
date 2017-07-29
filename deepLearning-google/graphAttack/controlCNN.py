import graphAttack as ga
import numpy as np
import pickle
import tensorflow as tf
"""Control script"""


pickleFilename = "testDataTensor.pkl"
with open(pickleFilename, "rb") as fp:
    X, Y = pickle.load(fp)


inputTens = X[0:1]
outputTens = None
filterTensor = np.random.random((10, 10, X.shape[3], 2))

graph = tf.Graph()
with graph.as_default():
    con = tf.nn.conv2d(inputTens, filterTensor, [1, 1, 1, 1], "SAME")

with tf.Session(graph=graph) as session:
    tf.global_variables_initializer().run()
    conVal = con.eval()