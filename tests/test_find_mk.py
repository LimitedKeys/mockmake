

from itertools import zip_longest

import pytest

import scripts.find_mk as find_mk

def test_find_source_src1(src1):
    root, files = src1
    result = find_mk.find_source(root)

    for expected, actual in zip_longest(
            files, 
            result):
        assert expected == actual
