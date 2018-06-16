"""Tools ot load in and pre-process the dataset"""
import dataset.get_dataset as gd
from dataset.parallel import parallel_control, paralll_worker
from dataset.storage import load_pickle_object, save_pickle_object
from dataset.preprocess import hash_document, get_3gram_lookap, cleanup_document, hash_word
import pandas as pd
import numpy as np

def main():
    df = gd.load_reviews()
    df.to_csv("/Users/golejace/Documents/coding-workspace/python-mxnet/ibdm/aclImdb/reviews_data_clean.csv", index=False)
    # df = pd.read_csv("/Users/golejace/Documents/coding-workspace/python-mxnet/ibdm/aclImdb/reviews_data.csv")
    #
    # vocabulary = "0abcdefghijklmnopqrstuvwxyz"
    # n_gram_lookap = get_3gram_lookap(vocabulary)
    # dataset = gd.generate_dataset(df.loc[0: 1000, :], n_gram_lookap)
    # dataset = gd.generate_dataset_parallel(df, n_gram_lookap)
    # save_pickle_object(dataset, "aclImdb/dataset.pkl")

    # vocabulary = "ab"
    # n_gram_lookap = get_3gram_lookap(vocabulary)
    # docu = hash_document("ababa", n_gram_lookap)
    # print(np.nonzero(docu.toarray()))
    # print(docu.toarray())
    # print(n_gram_lookap)




def profile_main():
    """Profile the function"""
    from line_profiler import LineProfiler
    lp = LineProfiler()

    functions = [main,
                 parallel_control, paralll_worker,
                 gd.generate_dataset, gd.generate_datapoint, hash_document, hash_word]

    for fnc in functions:
        lp.add_function(fnc)

    lp_wrapper = lp(main)
    result = lp_wrapper()
    lp.print_stats()


if (__name__ == "__main__"):
    profile_main()