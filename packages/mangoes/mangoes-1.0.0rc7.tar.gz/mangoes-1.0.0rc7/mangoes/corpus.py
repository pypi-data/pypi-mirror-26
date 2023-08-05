# -*- coding: utf-8 -*-
"""
Class and functions to manage the documents used as corpus.
"""

import collections
import logging
import os.path
import pickle

import mangoes.utils
import mangoes.utils.decorators
import mangoes.utils.exceptions
import mangoes.utils.io
import mangoes.utils.reader
from mangoes.utils.options import ProgressBar

_logger = logging.getLogger(__name__)

TEXT = mangoes.utils.reader.TextSentenceGenerator
BROWN = mangoes.utils.reader.BrownSentenceGenerator
XML = mangoes.utils.reader.XmlSentenceGenerator
CONLL = mangoes.utils.reader.ConllSentenceGenerator


class Corpus:
    """Class to access to the source used as a Corpus

    The Corpus class creates a sentence generator from documents.


    Parameters
    ----------
    content : a string or an iterable
        An iterable of sentences or a path to a file or a repository
    name: str
        A name for your corpus.
        If no name is given and content is a path, the name will be this path.
    reader : class
        A class deriving from :class:`mangoes.utils.reader.SentenceGenerator`.
        Some shortcuts are defined in this module : TEXT (default), BROWN, XML and CONLL
    filter_attributes : string or tuple
        If the source is annotated, tuple or list of attributes to read. If None (default), all attributes are read.
        This parameter is not compatible with reader = TEXT
    lower : boolean, optional
        If True, converts sentences to lower case. Default : False
    digit : boolean, optional
        If True, replace numeric values with the value of `DIGIT_TOKEN` in sentences. Default : False
    nb_sentences : int (optional)
        Expected number of sentences in Corpus, if known. This number is used to improve the output of the
        progress bar but the real value will be computed when initialized.
    lazy : boolean (optional)
        if False (default), count words and sentences when creating the Corpus (that can take a while);
        if True, only count words and sentences when needed.

    Attributes
    ----------
    words_count : collections.Counter
    nb_sentences
    size

    """

    def __init__(self, content, name=None, language=None, reader=TEXT, filter_attributes=None,
                 lower=False, digit=False, nb_sentences=None, lazy=False):

        self._logger = logging.getLogger("{}.{}".format(__name__, self.__class__.__name__))

        self.content = content
        self.reader = reader(content, lower, digit, filter_attributes)
        self._reader_class = reader

        self._words_count = None
        self._size = None
        self._nb_sentences = nb_sentences

        if not name and isinstance(content, str) and os.path.exists(content):
            name = content

        self._params = {"lower": lower, "digit": digit, "filter_attributes": filter_attributes,
                        "name": name, "language": language}

        if not lazy:
            self._count_words()

    def __iter__(self):
        return self.reader.sentences()

    @property
    def nb_sentences(self):
        """Number of sentences in this corpus or None if unknown.

        Returns
        -------
        int or None

        Notes
        ------

        If Corpus is created with parameter lazy=True, this value is evaluated only when words_count is called.
        The value may also be set manually (if it is known).

        """
        return self._nb_sentences

    @nb_sentences.setter
    def nb_sentences(self, nb):
        self._nb_sentences = nb

    @property
    def name(self):
        """Name of the corpus"""
        return self._params["name"]

    @property
    def lower(self):
        """If True, converts sentences to lower case."""
        return self._params["lower"]

    @property
    def digit(self):
        """If True, replace numeric values with the value of `DIGIT_TOKEN` in sentences."""
        return self._params["digit"]

    @property
    def filter_attributes(self):
        """If the source is annotated, tuple or list of attributes to read."""
        return self._params["filter_attributes"]

    @property
    def params(self):
        """Parameters of the corpus"""
        return self._params

    @property
    def words_count(self):
        """Occurrences of each word in the corpus

        Returns
        -------
        collections.Counter
            a Counter with words as keys and number of occurrences as value

        """
        if self._words_count is None:
            self._count_words()
        return self._words_count

    @property
    def size(self):
        """Number of words in the Corpus

        Returns
        -------
        int

        """
        if self._size is None:
            self._size = sum(self.words_count.values())

        return self._size

    def create_vocabulary(self, attributes=None, filters=None):
        """Create a vocabulary from the corpus

        Parameters
        ----------
        attributes : string or tuple of string, optional
            If the Corpus is annotated, attribute(s) to get for each token. If None (default), all attributes are kept.
        filters : list of callables, optional
            A filter is a parametrized function that filter values from the Corpus' ``words_count``. This module
            provides 4 filters :
                * :func:`truncate`
                * :func:`remove_least_frequent`
                * :func:`remove_most_frequent`
                * :func:`remove_elements`

        Returns
        -------
        mangoes.Vocabulary

        Notes
        ------
        You can also write and use your own filters. A filter is a parametrized function that takes a
        ``collections.Counter()`` as input and returns a ``collections.Counter()``.
        It should be decorated with :func:`mangoes.utils.decorators.counter_filter`

        """
        if attributes:
            words = collections.Counter()
            for token in self.words_count:
                words[get_attributes_from_token(token, attributes)] += self.words_count[token]
        else:
            words = self.words_count

        if filters:
            for filter_ in filters:
                words = filter_(words)

        return mangoes.Vocabulary(list(words.keys()), entity=attributes, language=self.params["language"])

    def save_metadata(self, file_path):
        """Save metadata of this Corpus in a pickle file

        Save path to corpus, words_count, number of sentences, ... in a pickle file

        Parameters
        ----------
        file_path : string

        """
        with open(file_path, 'wb') as pickle_file:
            pickle.dump(self, pickle_file)

    @staticmethod
    def load_from_metadata(file_path):
        """Create a Corpus instance from previously saved metadata

        Parameters
        ----------
        file_path : string
        """
        with open(file_path, 'rb') as pickle_file:
            return pickle.load(pickle_file)

    @mangoes.utils.decorators.timer(display=_logger.info, label="counting occurrences of each word in corpus")
    def _count_words(self):
        self._words_count = collections.Counter()
        real_nb_sentences = 0

        for sentence in ProgressBar(self, total=self._nb_sentences):
            self._words_count.update(sentence)
            real_nb_sentences += 1

        self._nb_sentences = real_nb_sentences

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['_logger']
        del state['reader']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self._logger = logging.getLogger("{}.{}".format(__name__, self.__class__.__name__))
        self.reader = self._reader_class(self.content, self.lower, self.digit, self.filter_attributes)


# ##############################################
# Filters to select vocabulary from a corpus

@mangoes.utils.decorators.counter_filter
def truncate(max_nb, words_count):
    """Filter to apply to a counter to keep at most 'max_nb' elements.

    Elements with higher counts are preferred over elements with lesser counts.
    Elements with equal counts are arbitrarily selected during the truncating, if necessary.

    Parameters
    ----------
    max_nb: positive int
        Maximal number of elements to keep
    words_count: collections.Counter
        The counter to filter

    Returns
    --------
    collections.Counter

    See Also
    ----------
    :class:`mangoes.vocabulary.Vocabulary`
    :func:`mangoes.utils.decorators.counter_filter`


    """
    return collections.Counter({word: frequency
                                for (word, frequency) in words_count.most_common(max_nb)})


@mangoes.utils.decorators.counter_filter
def remove_least_frequent(min_frequency, words_count):
    """Filter to apply to a counter to keep the elements with a high enough frequency.

    Parameters
    ----------
    min_frequency: positive int or float
        If >= 1, will be interpreted as a 'count' value (a positive integer), else,
        will be interpreted as a frequency.
    words_count: collections.Counter
        The counter to filter

    Returns
    --------
    collections.Counter

    Examples
    ---------
    >>> vocabulary = mangoes.Vocabulary(corpus,
    >>>                                filters=[mangoes.vocabulary.remove_least_frequent(min_frequency)])

    See Also
    ----------
    :class:`mangoes.vocabulary.Vocabulary`
    :func:`mangoes.utils.decorators.counter_filter`
    """

    if min_frequency >= 1:
        return collections.Counter({w: freq
                                    for w, freq in words_count.items() if freq >= min_frequency})
    if min_frequency >= 0:
        total_number = float(sum(words_count.values()))
        return collections.Counter({w: freq
                                    for w, freq in words_count.items() if
                                    freq / total_number >= min_frequency})

    raise mangoes.utils.exceptions.NotAllowedValue(msg="'min_frequency' parameter value must be positive "
                                                       "(value = {}".format(min_frequency))


@mangoes.utils.decorators.counter_filter
def remove_most_frequent(max_frequency, words_count):
    """Filter to apply to a counter to only keep the elements with a low enough frequency.

    Parameters
    ----------
    max_frequency: positive int or float
        If >= 1, will be interpreted as a 'count' value (a positive integer), else,
        will be interpreted as a frequency.
    words_count: collections.Counter
        The counter to filter

    Returns
    --------
    collections.Counter

    Examples
    ---------
    >>> vocabulary = mangoes.Vocabulary(corpus,
    >>>                                filters=[mangoes.vocabulary.remove_most_frequent(max_frequency)])

    See Also
    ----------
    :class:`mangoes.vocabulary.Vocabulary`
    :func:`mangoes.utils.decorators.counter_filter`
    """
    if max_frequency >= 1:
        return collections.Counter(
            {w: freq for w, freq in words_count.items() if freq <= max_frequency})
    elif max_frequency >= 0:
        total_number = float(sum(words_count.values()))
        return collections.Counter(
            {w: freq for w, freq in words_count.items() if freq / total_number <= max_frequency})

    raise mangoes.utils.exceptions.NotAllowedValue(msg="'max_frequency' parameter value must be positive "
                                                       "(value = {}".format(max_frequency))


@mangoes.utils.decorators.counter_filter
def remove_elements(stopwords, words_count=None, attribute=None):
    """Filter to apply to a counter to remove the elements in 'stopwords' set-like object.

    Parameters
    -----------
    stopwords: list or set or string
        collection of words to remove from the words_count
        (ex: nltk.corpus.stopwords.words("english") or string.punctuation)
    attribute: str or tuple, optional
        If the keys in words_count are annotated tokens, attribute to consider
    words_count: collections.Counter
        The counter to filter

    Returns
    --------
    collections.Counter

    See Also
    ----------
    :class:`mangoes.vocabulary.Vocabulary`
    :func:`mangoes.utils.decorators.counter_filter`
    """
    if attribute:
        return collections.Counter({w: freq for w, freq in words_count.items()
                                    if get_value_of_attribute_from_token(w, attribute) not in stopwords})
    return collections.Counter({w: freq for w, freq in words_count.items() if w not in stopwords})


######################
# Tokens

def get_attributes_from_token(token, attributes):
    """Extract attributes from a token

    Parameters
    ----------
    token : string
        A string formatted like "tag_1:value_1/tag2:value_2/.../tag_n:value_n"
    attributes : string or tuple of strings
        The attributes to extract

    Returns
    -------
    string

    Examples
    --------
    >>> mangoes.corpus.get_attributes_from_token("word:are/pos:V/lemma:be", attributes="lemma")
    'lemma:be'
    >>> mangoes.corpus.get_attributes_from_token("word:are/pos:V/lemma:be", attributes=("pos", "lemma"))
    'pos:V/lemma:be'
    """
    return "/".join([attribute for attribute in token.split('/') if attribute.split(':', 1)[0] in attributes])


def get_value_of_attribute_from_token(token, attribute_name):
    """Extract the value of one attribute from a token

    Parameters
    ----------
    token : string
        A string formatted like "tag_1:value_1/tag2:value_2/.../tag_n:value_n"
    attribute_name : string
        The attribute to extract

    Returns
    -------
    string

    Examples
    --------
    >>> mangoes.corpus.get_value_of_attribute_from_token("word:are/pos:V/lemma:be", "lemma")
    'be'
    """
    try:
        for attribute in token.split('/'):
            name, value = attribute.split(":", 1)
            if name == attribute_name:
                return value
    except ValueError:
        # TODO : the word contains "/" or ":"
        pass
