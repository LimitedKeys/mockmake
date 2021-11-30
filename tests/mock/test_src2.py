
import os
import subprocess

import pytest

def test_mock(src2):
    path, _ = src2
    subprocess.run([
        "make -f {}/Makefile".format(path)],
        check=True,
        shell=True,
        )
