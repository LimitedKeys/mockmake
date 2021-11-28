 
import pathlib

import pytest

@pytest.fixture(scope="session")
def src1(tmpdir_factory):
    files = []
    root = tmpdir_factory.mktemp("src1")

    files.append(pathlib.Path(root / "a.c"))

    for some_file in files:
        some_file.touch()

    return root, files
