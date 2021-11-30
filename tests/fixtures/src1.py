
import os
import pathlib

import pytest

from tests.defines import MOCK_MK

@pytest.fixture(scope="session")
def src1(tmpdir_factory):
    files = []
    root = tmpdir_factory.mktemp("src1")

    main = pathlib.Path(root / "a.c")
    files.append(main)

    with open(main, 'w') as out:
        out.write('\n'.join([
            '#include <stdio.h>',
            '',
            'int main(void) {',
            '    printf("Hello, World");',
            '    return 0;',
            '}',
            ]))

    with open(root / 'Makefile', 'w') as out:
        out.write('\n'.join([
            'MOCK_OUTPUT = {}'.format(root / 'output'),
            'MOCK_SOURCE = {}'.format(root),
            'MOCK_INCLUDE = {}'.format(root),
            '',
            '.PHONY: all',
            '',
            'include {}'.format(MOCK_MK),
            '',
            'all: mock_run',
            '',
            ]))

    return root, files
