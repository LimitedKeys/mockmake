
import os
import subprocess

import pytest

def test_mock(src1):
    path, _ = src1
    subprocess.run([
        "make -f {}/Makefile".format(path)],
        check=True,
        shell=True,
        )
