
import os
import pathlib
import argparse

C_EXTENSIONS = ['.c', '.s', '.cpp']

def find_source(root):
    ''' Find all C source files from the provided root directory.

    Args:
        root (Path): path to the directory to search

    Returns:
        List of found source files.
    '''
    found = []

    for path in pathlib.Path(root).glob('**/*'):
        extension = path.suffix
        if extension in C_EXTENSIONS:
            found.append(path.resolve())

    return found

def main():
    parser = argparse.ArgumentParser("Find sourse files")

    parser.add_argument("source_dirs")
    parser.add_argument("include_dirs")
    parser.add_argument("output_file")

    args = parser.parse_args()

    source_dirs = [i.strip() for i in args.source_dirs.split()]

    include_dirs = ['-I{}'.format(i.strip()) for i in args.include_dirs.split()]
    includes = ' '.join(include_dirs)

    all_sources = []
    for some_dir in source_dirs:
        if some_dir:
            all_sources.extend(find_source(some_dir))

    all_objs = []
    for i in all_sources:
        name, _ = os.path.splitext(os.path.basename(i))
        obj = name + '.o'
        all_objs.append(os.path.join(
            '$(MOCK_OUTPUT)',
            obj))

    output_path = os.path.join(args.output_file)

    with open(output_path, 'w') as output:
        output.write('\n'.join([
            "# Generated by source_mk",
            '',
            "FIND_OBJS := {}".format(' '.join(all_objs)),
            "FIND_SRC  := {}".format(' '.join([str(i) for i in all_sources])),
            "FIND_INCLUDES := {}".format(includes),
            '',
            ]))

        for src, obj in zip(all_sources, all_objs):
            output.write(f'{obj}: {src}\n')
            output.write(f"\t$(CC) -c {src} -o {obj} {includes}\n")
            output.write("\n")

if __name__== "__main__":
    main()
