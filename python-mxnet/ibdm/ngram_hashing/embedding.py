"""This is a class with the base implementation fo the word embedding tool"""
import heapq
import numpy as np


class WordEmbeddingNGramHashing(object):
    """
    This is the word embedding model based on n-gram hashing

    Parameters
    ----------
    max_ngram : int
        Maximum n-gram length to use for the embedding
    vocab_length : int
        maximum number of variuos n-grams to use for embeding
    """

    def __init__(self, max_ngram=4, vocab_length=2000, fix_onegrams=False):
        self.max_ngram = max_ngram
        self._full_lookup = {}
        self._final_lookup = None
        self.bow = "<"
        self.eow = ">"

        if fix_onegrams:
            self.training_min_ngram = 2
            self.extra_vocab = [item for item in "0123456789abcdefghijklmnopqrstuvwxyz"]
            self.vocab_length = vocab_length - len(self.extra_vocab)
        else:
            self.training_min_ngram = 1
            self.extra_vocab = []
            self.vocab_length = vocab_length

    def __repr__(self):
        """
        Print some statistics about the embedding
        """
        result = "This is the n-gram hash embedding with\n"
        result += "maxn: {}, vocab_length: {}, bow: |{}|, eow: |{}|\n".format(self.max_ngram,
                                                                              self.vocab_length,
                                                                              self.bow,
                                                                              self.eow)
        if self._final_lookup is None:
            result += "It is not yet trained"
        else:
            for n in range(1, self.max_ngram + 1):
                number_n_grams = sum(1 for item in self._final_lookup if len(item) == n)
                result += "Number of {}-grams: {}\n".format(n, number_n_grams)

        return result

    def train_update_from_list(self, corpus):
        """
        Update the internal lookup table with new words from the corpus
        WARNING: beggining_of_word and end_of_word signs are added

        Parameters
        ----------
        corpus : iterable[str]
            Document corpus given as a iterable of documents
        """
        for document in corpus:
            for word in document.split():
                word = self.bow + word + self.eow
                for n in range(self.training_min_ngram, self.max_ngram + 1):
                    for ngram in ngramify(word, n):
                        try:
                            self._full_lookup[ngram] += 1
                        except KeyError:
                            self._full_lookup[ngram] = 1

    def train_finalise(self):
        """
        Finalise the training by only retaining vocab_length most popular
        n_grams and assign ids to them

        """
        self._final_lookup = {}
        vocab = heapq.nlargest(self.vocab_length, self._full_lookup, key=lambda inp: self._full_lookup[inp])
        vocab = self.extra_vocab + vocab
        self.vocab_length = len(vocab)
        for idx, ngram in enumerate(vocab):
            self._final_lookup[ngram] = idx


    def check_collisions(self, corpus):
        """
        Check for collisions in the corpus.

        Parameters
        ----------
        corpus : iterable[str]
            Vocabulary corpus given as an iterable of words
        """
        num_words = len(corpus)
        embedded_corpus = np.empty((num_words, self.vocab_length))

        for idx, word in enumerate(corpus):
            embedded_corpus[idx, :] = self.word_embedding(str(word))[:]
        n_unique = np.unique(embedded_corpus, axis=0).shape[0]
        collisions = num_words - n_unique
        return collisions / num_words, collisions, num_words



    def word_embedding(self, word):
        """Return an embedded vector for a given word
        WARNING: beggining_of_word and end_of_word signs are added

        Parameters
        ----------
        word : str
            Word to be embedded

        Returns
        -------
        ndarray
            The vector representation of a word
        """

        result = np.zeros(self.vocab_length)
        word = self.bow + word + self.eow
        for n in range(1, self.max_ngram + 1):
            for ngram in ngramify(word, n):
                try:
                    result[self._final_lookup[ngram]] += 1
                except KeyError:
                    pass

        return result

    def in_dictionary(self, word):
        """
        Check if a word is in the dictionary

        Parameters
        ----------
        word : str
            Word to be checked

        Returns
        -------
        bool
        """
        return True

    def get_vector_dim(self):
        """
        Return the dimension of word emedding vector

        Returns
        -------
        float
            The embedding vector should be (n_dims, )
        """
        return self.vocab_length

    def document_embedding(self, document, return_document=False):
        """
        Embed a whole document given as a list of words

        Parameters
        ----------
        document : list[str]
            List of words in the document
        return_document : bool
            If true, return the document without any oov words

        Returns
        -------
        List[ndarray]
            embedded document
        List[str]
            document without any oov words

        """

        embedded = []
        for word in document:
            try:
                embedded.append(self.word_embedding(word))
            except KeyError:
                pass

        if return_document:
            document = [word for word in document if self.in_dictionary(word)]
            return embedded, document
        else:
            return embedded

    def remove_document_oov(self, document):
        """
        remove out of vocabulary (oov) words from the document

        Parameters
        ----------
        document : list[str]
            List of words in the document

        Returns
        -------
        List[str]
            document without any oov words

        """
        return document


def ngramify(word, n):
    """
    Convert a string into an character n-grams iterable

    Parameters
    ----------
    word : str
        String to n-gramify
    n : int
        Length of the individual chunk

    Returns
    -------
    iterable
        list of n-grams
    """
    if n == 0:
        return None

    num_ngrams = len(word) - n + 1
    for idx in range(num_ngrams):
        yield word[idx: idx + n]
