"""Tools ot load in and pre-process the dataset"""
import multiprocessing as mp
import math
import os
import pandas as pd
from dataset.preprocess import cleanup_document, hash_document
from dataset.storage import save_pickle_object
from dataset.parallel import parallel_control

DATASET_PREFIX = "/Users/golejace/Documents/coding-workspace/python-mxnet/ibdm/aclImdb"


def load_reviews():
    level0 = ["train", "test"]
    level1 = ["pos", "neg"]
    list2process = []
    for l0 in level0:
        for l1 in level1:
            for element in os.listdir(os.path.join(DATASET_PREFIX, l0, l1)):
                list2process.append((l0, l1, element))

    fixed_argument = (True, )
    reviews = parallel_control(load_review, list2process, fixed_args=fixed_argument, num_threads=2)
    reviews = [item[1] for item in reviews]
    df = pd.DataFrame(reviews, columns=["id", "sentiment", "review"])
    return df


def generate_dataset(df, n_gram_lookap):
    """Generate the dataset from a dataframe of raw inputs"""
    dataset = [generate_datapoint(df.loc[idx, "sentiment"],
                                  df.loc[idx, "review"],
                                  n_gram_lookap) for idx in df.index]
    return dataset


def generate_dataset_parallel(df, n_gram_lookap, num_threads=2):
    list2process = [(df.loc[idx, "sentiment"], df.loc[idx, "review"]) for idx in df.index]
    fixed_argument = (n_gram_lookap, )
    dataset = parallel_control(generate_datapoint, list2process, fixed_args=fixed_argument, num_threads=num_threads)
    dataset = [item[1] for item in dataset]
    return dataset


def generate_datapoint(score, document, n_gram_lookap):
    """Tokenize and hash the review and produce a dataset
    [tuple(score: int, review: ndarray)]
    """
    document = cleanup_document(document)
    hash_array = hash_document(document, n_gram_lookap)
    return hash_array, score


def load_review(set_dir, sentiment_dir, filename, cleanup=False):
    """
    Load the dataset and return a tuple with
    review_id, sentiment, raw_review
    """

    if sentiment_dir == "pos":
        sentiment = 1
    elif sentiment_dir == "neg":
        sentiment = 0
    else:
        raise ValueError("sentiment_dir must be pos or neg")
    id = filename[:-4]

    path = os.path.join(DATASET_PREFIX, set_dir, sentiment_dir, filename)
    with open(path, "r") as fp:
        review = fp.read()

    review = cleanup_document(review)
    return id, sentiment, review
