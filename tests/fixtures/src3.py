
import os
import pathlib

import pytest

from tests.defines import MOCK_MK

@pytest.fixture(scope="session")
def src3(tmpdir_factory):
    files = []
    root = tmpdir_factory.mktemp("src3")
    lib = root / 'lib'
    lib.mkdir()

    dir1 = lib / 'a'
    dir1.mkdir()

    dir2 = lib / 'b'
    dir2.mkdir()

    dir3 = lib / 'c'
    dir3.mkdir()

    dir4 = root / 'src'
    dir4.mkdir()

    sources = [str(lib), str(dir4)]
    include = [str(lib), str(dir4)]

    some_file = pathlib.Path(dir1 / "a.h")
    with open(some_file, 'w') as out:
        out.write('\n'.join([
            '#ifndef A_H',
            '#define A_H',
            '',
            'void printa(void);',
            '',
            '#endif  // A_H',
            ]))

    some_file = pathlib.Path(dir1 / "a.c")
    files.append(some_file)
    with open(some_file, 'w') as out:
        out.write('\n'.join([
            '#include <stdio.h>',
            '#include "a/a.h"',
            '',
            'void printa(void) {',
            '    printf("A");',
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

    some_file = pathlib.Path(dir4 / 'main.c')
    files.append(some_file)
    with open(some_file, 'w') as out:
        out.write('\n'.join([
            '#include "a/a.h"',
            '#include "b/b.h"',
            '#include "c/c.h"',
            '',
            'int main(void) {',
            '    printa();',
            '    printb();',
            '    printc();',
            '}',
            ]))

    with open(root / 'Makefile', 'w') as out:
        out.write('\n'.join([
            'MOCK_OUTPUT = {}'.format(str(root / 'output')),
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
