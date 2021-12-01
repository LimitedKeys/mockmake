
import subprocess

import pytest

def test_mock(src3):
    path, _ = src3
    subprocess.run([
        "make -f {}/Makefile".format(path)],
        check=True,
        shell=True,
        )
