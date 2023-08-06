# -*- coding: utf-8 -*-
"""

Low level API for loading of word embedding file that was implemented in
`word2vec <https://code.google.com/archive/p/word2vec/>`_, by Mikolov.
This implementation is for word embedding file created with ``-binary 1``
option.
"""
from __future__ import absolute_import, division, print_function, \
    unicode_literals

from collections import OrderedDict

import ctypes
from libc.stdio cimport FILE, fscanf, fread, fdopen
import numpy as np
cimport numpy as np
from cpython cimport bool

from word_embedding_loader import ParseError, parse_warn

ctypedef np.float32_t FLOAT


def check_valid(line0, line1):
    """
    Check :func:`word_embedding_loader.loader.glove.check_valid` for the API.
    """
    # Only check the first line
    data0 = line0.split(b' ')
    if len(data0) != 2:
        return False
    # check if data0 is int values
    try:
        map(int, data0)
    except:
        return False
    return True


cdef _load_with_vocab_impl(FILE *f, vocabs, long long size):
    cdef char ch
    cdef int l
    cdef char[100] vocab
    cdef int words = len(vocabs)
    cdef np.ndarray[FLOAT, ndim=2, mode="c"] arr = np.empty([words, size], dtype=np.float32)
    cdef np.ndarray[FLOAT, ndim=2, mode="c"] dummy = np.empty([1, size], dtype=np.float32)
    cdef int i = 0
    cdef int idx
    while True:
        if i == words:
            break
        # Remove any new line/spaces between vocabulary
        fscanf(f, "%*[ \n\r]")
        fscanf(f, "%s%n%c", &vocab, &l, &ch)
        ustring = <bytes>vocab[:l]
        if ustring in vocabs:
            idx = vocabs[ustring]
            fread(&arr[idx, 0], sizeof(FLOAT), size, f)
            # Word counting does not take duplicated words in consideration
            i += 1
        else:
            fread(&dummy[0, 0], sizeof(FLOAT), size, f)
    return arr


def load_with_vocab(fin, vocab, dtype=np.float32):
    """
    Refer to :func:`word_embedding_loader.loader.glove.load_with_vocab` for the API.
    """
    cdef FILE *f = fdopen(fin.fileno(), 'rb') # attach the stream
    if (f) == NULL:
       raise IOError()
    cdef long long words, size
    fscanf(f, '%lld', &words)
    fscanf(f, '%lld', &size)
    ret = _load_with_vocab_impl(f, vocab, size)
    return ret.astype(dtype)


cdef _load_impl(FILE *f, long long words, long long size):
    cdef char ch
    cdef int l
    cdef char[100] vocab
    vocabs = dict()
    cdef np.ndarray[FLOAT, ndim=2, mode="c"] arr = np.zeros([words, size], dtype=np.float32)
    cdef int i = 0
    while True:
        if i >= words:
            break
        # Remove any new line/spaces between vocabulary
        fscanf(f, "%*[ \n\r]")
        fscanf(f, "%s%n%c", &vocab, &l, &ch)
        vocabs[<bytes>vocab[:l]] = i
        fread(&arr[i, 0], sizeof(FLOAT), size, f)
        i += 1
    return arr, vocabs


def load(fin, dtype=np.float32, max_vocab=None):
    """
    Refer to :func:`word_embedding_loader.loader.glove.load` for the API.
    """
    cdef FILE *f = fdopen(fin.fileno(), 'rb') # attach the stream
    if (f) == NULL:
       raise IOError()
    cdef long long words, size
    fscanf(f, '%lld', &words)
    fscanf(f, '%lld', &size)
    if max_vocab is None:
        words = words
    else:
        words = min(max_vocab, words)
    ret = _load_impl(f, words, size)
    arr, vocabs = ret
    return arr.astype(dtype), vocabs
