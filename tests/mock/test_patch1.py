
import subprocess

import pytest

def test_mock(patch1):
    path, _ = patch1
    subprocess.run([
        "make -f {}/Makefile".format(path)],
        check=True,
        shell=True,
        )
