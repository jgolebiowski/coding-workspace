"""Tools preprocess a text string for further analysis"""
from bs4 import BeautifulSoup
import string
import unicodedata
import re
import numpy as np
import scipy.sparse
import mxnet as mx

PUNCTUATION_TABLE = str.maketrans({key: " " for key in string.punctuation})


def cleanup_document(document):
    """Clean up the document with the following operations
    1. Decode HTML markup
    2. Remove @xx twitter mentions
    3. Remove links
    4. Recode as ascii
    5. Lowercase
    6. Remove contractions
    7. Remove punctuation
    8. Convert all numbes to 0
    9. Clean up extra whitespace

    Parameters
    ----------
    document : str
        The document to be cleaned up

    Returns
    -------
    str
        Cleaned up document

    """
    # Decode HTML
    document = BeautifulSoup(document, "html.parser").get_text()

    # Remove twitter mentions
    document = re.sub(r'@[A-Za-z0-9]+', '', document)

    # Remove links
    re.sub('https?://[A-Za-z0-9./]+', '', document)

    # Try to recode as ascii
    try:
        document = str(unicodedata.normalize('NFKD', document).encode('ascii', 'ignore'))
        document = re.sub(r'[\x00-\x1F]+', '', document)
    except:
        pass

    # Lowercase
    document = document.lower()

    # Remove specific contractions
    document = re.sub(r"won't", "will not", document)
    document = re.sub(r"can\'t", "can not", document)

    # Remove general contractions
    document = re.sub(r"n\'t", " not", document)
    document = re.sub(r"\'re", " are", document)
    document = re.sub(r"\'s", " is", document)
    document = re.sub(r"\'d", " would", document)
    document = re.sub(r"\'ll", " will", document)
    document = re.sub(r"\'t", " not", document)
    document = re.sub(r"\'ve", " have", document)
    document = re.sub(r"\'m", " am", document)

    # Convert all numbers to 0
    document = re.sub(r"[0-9]+", "0", document)

    # Remove punctuation
    document = document.translate(PUNCTUATION_TABLE)

    # Remove all extra whitespace
    document = re.sub('\s+', ' ', document).strip()
    return document


def get_3gram_lookap(vocabulary):
    """
    Produce an 3-gram lookup dictionary from vocabulary.
    Uses all letters in the vocabulary and special characters
        start of word token: <
        end of word token: >

    Parameters
    ----------
    vocabulary : str
        List of characters to be included

    Returns
    -------
    dict[str: int]
        The dictionary used for hashing, this must include all possible 3-grams
        of letters in vocab and extra characters.
    """
    if len(vocabulary) != len(set(vocabulary)):
        raise ValueError("Duplicate entry in the vocabulary")
    if "<" not in vocabulary:
        vocabulary  = "<" + vocabulary
    if ">" not in vocabulary:
        vocabulary += ">"

    index = 0
    ngram_lookap = {}
    for a in vocabulary:
        for b in vocabulary:
            for c in vocabulary:
                ngram_lookap[a + b + c] = index
                index += 1

    return ngram_lookap


def ngramify(word, n):
    """
    Convert a string into an character n-grams list

    Parameters
    ----------
    word : str
        String to n-gramify
    n : int
        Length of the individual chunk

    Returns
    -------
    list[str]
        List of n-grams
    """
    if n == 0:
        return None

    num_ngrams = max(1, len(word) - n + 1)
    return [word[idx: idx + n] for idx in range(num_ngrams)]


def hash_word(word, ngram_lookap):
    """
    Hash a single word into character tri-grams.

    Parameters
    ----------
    word : str
        The word to be hashed
    ngram_lookap : dict[str: int]
        The dictionary used for hashing, this must include all possible 3-grams
        of letters in vocab and extra characters:
        start of word token: <
        end of word token: >

    Returns
    -------
    indexes : list[int]
    data : list[int]
        Data for the bag-of-trigrams representation of the word where
        resulting_array[indexes[k]] = data[k]
    n_entries : int
        Number of datapoints in the output array
    """
    n_in_ngram = 3
    trigram_list = dict()
    indexes = []
    data = []

    for trigram in ngramify(word, n_in_ngram):
        try:
            trigram_list[trigram] += 1
        except KeyError:
            trigram_list[trigram] = 1

    for trigram, n_occur in trigram_list.items():
        try:
            trigram_idx = ngram_lookap[trigram]
        except KeyError:
            raise KeyError("Trigram |{}| not in the ngram_lookup!".format(trigram))

        indexes.append(trigram_idx)
        data.append(n_occur)

    return indexes, data, len(data)


def hash_document(document, ngram_lookap):
    """
    Hash a document word-by-wordinto character level tri-grams following
    the method discussed in

    Learning Deep Structured Semantic Models for Web Search using Clickthrough Data
    Po-Sen Huang
    Xiaodong He
    Jianfeng Gao
    Li Deng
    Alex Acero
    Larry Heck

    Parameters
    ----------
    document : str
        The document to be cleaned up
    ngram_lookap : dict[str: int]
        The dictionary used for hashing, this must include all possible 3-grams
        of letters in vocab and extra characters:
        start of word token: <
        end of word token: >

    Returns
    -------
    scipy.sparse.csr_matrix
        Array with the output document, the shapes are
        (vocab_size, document_length)
    """
    tokenized_document = document.split()
    vocab_size = len(ngram_lookap)
    document_length = len(tokenized_document)

    row = []
    col = []
    data = []

    for word_idx, word in enumerate(tokenized_document):
        indexes, word_data, n_entries = hash_word("<" + word + ">", ngram_lookap)
        row += indexes
        col += [word_idx for i in range(n_entries)]
        data += word_data

    result = scipy.sparse.csr_matrix((data, (row, col)), shape=(vocab_size, document_length))
    # result = mx.nd.sparse.csr_matrix((data, (row, col)), shape=(vocab_size, document_length), dtype=np.float32)
    # print("original", result.shape)
    return result



