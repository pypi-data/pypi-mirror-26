# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, \
    unicode_literals

import os

import pytest


@pytest.fixture
def glove_file(tmpdir):
    with open(tmpdir.join('glove.txt').strpath, 'a+b') as f:
        f.write("""the 0.418 0.24968 -0.41242 0.1217
, 0.013441 0.23682 -0.16899 0.40951
日本語 0.15164 0.30177 -0.16763 0.17684""".encode('utf-8'))
        f.flush()
        f.seek(0)
        yield f


@pytest.fixture
def word2vec_bin_file_path():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(cur_dir, 'word2vec.bin')
    yield path


@pytest.fixture
def word2vec_bin_file(word2vec_bin_file_path):
    with open(word2vec_bin_file_path, 'rb') as f:
        yield f


@pytest.fixture
def word2vec_text_file(tmpdir):
    with open(tmpdir.join('word2vec_text_file.txt').strpath, 'a+b') as f:
        f.write("""3 2
</s> 0.080054 0.088388
the -1.420859 1.156857
日本語 -0.16799 0.10951""".encode('utf-8'))
        f.flush()
        f.seek(0)
        yield f


@pytest.fixture
def vocab_file(tmpdir):
    with open(tmpdir.join('vocab_file.txt').strpath, 'a+b') as f:
        f.write("""</s> 0
日本語 593677""".encode('utf-8'))
        f.flush()
        f.seek(0)
        yield f
