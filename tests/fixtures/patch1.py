
import pathlib

import pytest

@pytest.fixture(scope="session")
def patch1(src1):
    root, _ = src1

    # write patch
    patch_dir = root / 'scripts'
    patch_file = patch_dir / 'patch.py'
    patch_dir.mkdir()

    # read makefile, and add patch lines, and write it back
    with open(root / 'Makefile', 'r') as in_file:
        make_lines = in_file.readlines()

    make_lines.insert(0, "MOCK_PATCH = {}/main.c".format(str(root)))
    make_lines.insert(1, "MOCK_PSCRIPT = {}".format(str(patch_file)))

    with open(patch_file, 'w') as out:
        out.write('\n'.join([
            'import argparse',
            '',
            'def main():',
            '    parser = argparse.ArgumentParser()',
            '    parser.add_argument("in")',
            '    parser.add_argument("out")',
            '',
            '    args = parser.parse_args()',
            '',
            '    with open(args.in, "r") as f:',
            '        in_lines = f.readlines()',
            '',
            '    with open(args.out, "w") as f:',
            '        f.writelines(in_lines)',
            '',
            'if __name__ == "__main__":',
            '    main()',
            ]))

    return src1
