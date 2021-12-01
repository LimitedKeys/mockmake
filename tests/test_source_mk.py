

from itertools import zip_longest

import pytest

import scripts.source_mk as source_mk

def test_find_source_src1(src1):
    root, files = src1
    result = source_mk.find_source(root)

    for expected, actual in zip_longest(
            files, 
            result):
        assert expected == actual

def test_find_source_src2(src2):
    root, files = src2
    result = source_mk.find_source(root)

    for expected, actual in zip_longest(
            files, 
            result):
        assert expected == actual

def test_find_source_src3(src3):
    root, files = src3
    result = source_mk.find_source(root)

    for expected, actual in zip_longest(
            files, 
            result):
        assert expected == actual
