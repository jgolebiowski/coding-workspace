"""Tools ot load in and pre-process the dataset"""
from ngram_hashing.embedding import WordEmbeddingNGramHashing
import pandas as pd
import numpy as np

def main():
    df = pd.read_csv("/Users/golejace/Documents/coding-workspace/python-mxnet/ibdm/aclImdb/reviews_data_clean.csv")
    vocab_df = pd.read_csv("/Users/golejace/Documents/coding-workspace/python-mxnet/ibdm/aclImdb/imdb.vocab")

    for vocab_length in [200, 500, 1000, 2000]:
        embedding = WordEmbeddingNGramHashing(5, vocab_length, fix_onegrams=True)
        embedding.train_update_from_list(df.loc[:, "review"])
        embedding.train_finalise()
        print(embedding)

        col_freq, collisions, num_words = embedding.check_collisions(vocab_df.word)
        print(col_freq, collisions, num_words)

    # vocab_length = 40
    # embedding = WordEmbeddingNGramHashing(5, vocab_length, fix_onegrams=True)
    # embedding.train_update_from_list(df.loc[0: 200, "review"])
    # embedding.train_finalise()
    # print(embedding)
    # print(embedding._final_lookup)






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


if (__name__ == "__main__"):
    main()