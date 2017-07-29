import graphAttack as ga
import numpy as np
import pickle
import tensorflow as tf
"""Control script"""


pickleFilename = "testDataTensor.pkl"
with open(pickleFilename, "rb") as fp:
    X, Y = pickle.load(fp)

