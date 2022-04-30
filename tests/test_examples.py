
import os
import subprocess

import pytest 

PATH_HERE = os.path.dirname(__file__)

ROOT_PATH = os.path.abspath(
        os.path.join(PATH_HERE, ".."));

EXAMPLE_PATH = os.path.join(
        ROOT_PATH,
        "example")

EXAMPLES = [
    os.path.join(EXAMPLE_PATH, "firmware"),
    os.path.join(EXAMPLE_PATH, "hello_world"),
    os.path.join(EXAMPLE_PATH, "source_tree"),
    os.path.join(EXAMPLE_PATH, "includes"),
    os.path.join(EXAMPLE_PATH, "simple_patch"),
]

@pytest.mark.parametrize("path", EXAMPLES)
def test_build_example(path):
    subprocess.run([f"make -C {path} clean"],
            shell=True,
            check=True)
    subprocess.run([f"make -C {path}"],
            shell=True,
            check=True)
