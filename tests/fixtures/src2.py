
import os
import pathlib

import pytest

from tests.defines import MOCK_MK

@pytest.fixture(scope="session")
def src2(tmpdir_factory):
    files = []
    root = tmpdir_factory.mktemp("src2")

    dir1 = root / 'a'
    dir1.mkdir()

    dir2 = root / 'b'
    dir2.mkdir()

    dir3 = root / 'c'
    dir3.mkdir()

    sources = [dir1, dir2, dir3]
    sources = [str(i) for i in sources]
    include = [str(root)]

    main = pathlib.Path(dir1 / "a.c")
    files.append(main)

    with open(main, 'w') as out:
        out.write('\n'.join([
            '#include "b/b.h"',
            '#include "c/c.h"',
            '',
            'int main(void) {',
            '    printb();',
            '    printc();',
            '',
            '    return 0;',
            '}',
            ]))

    some_file = pathlib.Path(dir2 / "b.h")
    with open(some_file, 'w') as out:
        out.write('\n'.join([
            '#ifndef B_H',
            '#define B_H',
            '',
            'void printb(void);',
            '',
            '#endif  // B_H',
            ]))

    some_file = pathlib.Path(dir2 / "b.c")
    files.append(some_file)
    with open(some_file, 'w') as out:
        out.write('\n'.join([
            '#include <stdio.h>',
            '#include "b/b.h"',
            '',
            'void printb(void) {',
            '    printf("B");',
            '}',
            ]))

    some_file = pathlib.Path(dir3 / "c.h")
    with open(some_file, 'w') as out:
        out.write('\n'.join([
            '#ifndef C_H',
            '#define C_H',
            '',
            'void printc(void);',
            '',
            '#endif  // C_H',
            ]))

    some_file = pathlib.Path(dir3 / "c.c")
    files.append(some_file)
    with open(some_file, 'w') as out:
        out.write('\n'.join([
            '#include <stdio.h>',
            '#include "c/c.h"',
            '',
            'void printc(void) {',
            '    printf("C");',
            '}',
            ]))

    with open(root / 'Makefile', 'w') as out:
        out.write('\n'.join([
            'MOCK_OUTPUT = {}'.format(root / 'output'),
            'MOCK_SOURCE = {}'.format(' '.join(sources)),
            'MOCK_INCLUDE = {}'.format(' '.join(include)),
            '',
            '.PHONY: all',
            '',
            'include {}'.format(MOCK_MK),
            '',
            'all: mock_run',
            '',
            ]))

    return root, files
