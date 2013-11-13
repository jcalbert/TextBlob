# -*- coding: utf-8 -*-
'''Various tokenizer implementations.

.. versionadded:: 0.4.0
'''
from __future__ import absolute_import

from textblob.packages import nltk
from textblob.utils import strip_punc
from textblob.base import BaseTokenizer
from textblob.decorators import requires_nltk_corpus


class WordTokenizer(BaseTokenizer):

    '''NLTK's recommended word tokenizer (currently the TreeBankTokenizer).
    Uses regular expressions to tokenize text. Assumes text has already been
    segmented into sentences.

    Performs the following steps:

    * split standard contractions, e.g. don't -> do n't
    * split commas and single quotes
    * separate periods that appear at the end of line
    '''

    def tokenize(self, text, include_punc=True):
        '''Return a list of word tokens.

        :param text: string of text.
        :param include_punc: (optional) whether to include punctuation as separate tokens. Default to True.
        '''
        tokens = nltk.tokenize.word_tokenize(text)
        if include_punc:
            return tokens
        else:
            # Return each word token
            # Strips punctuation unless the word comes from a contraction
            # e.g. "Let's" => ["Let", "'s"]
            # e.g. "Can't" => ["Ca", "n't"]
            # e.g. "home." => ['home']
            return [word if word.startswith("'") else strip_punc(word, all=False)
                    for word in tokens if strip_punc(word, all=False)]


class SentenceTokenizer(BaseTokenizer):

    '''NLTK's sentence tokenizer (currently PunkSentenceTokenizer).
    Uses an unsupervised algorithm to build a model for abbreviation words,
    collocations, and words that start sentences,
    then uses that to find sentence boundaries.
    '''

    @requires_nltk_corpus
    def tokenize(self, text):
        '''Return a list of sentences.'''
        sentences = nltk.tokenize.sent_tokenize(text)
        return [s for s in sentences]
