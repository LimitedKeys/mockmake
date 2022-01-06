
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

def write_mk(path, includes, srcs, objs, patch_srcs, patch_targets):
    with open(path, 'w') as output:
        output.write('\n'.join([
            "# Generated by source_mk",
            '',
            "FIND_OBJS := {}".format(' '.join(objs)),
            "FIND_SRC  := {}".format(' '.join([str(i) for i in srcs])),
            "FIND_INCLUDES := {}".format(includes),
            '',
            ]))

        for src, obj in zip(srcs, objs):
            output.write(f'{obj}: {src}\n')
            output.write(f"\t$(CC) -c $(CFLAGS) $(CPPFLAGS) {src} -o {obj} {includes}\n")
            output.write("\n")

        for src, target in zip(patch_srcs, patch_targets):
            output.write(f'{target}: {src} $(MOCK_PSCRIPT)\n')
            output.write(f'\tpython $(MOCK_PSCRIPT) {src} {target}')
            output.write("\n")

def main():
    parser = argparse.ArgumentParser("Find sourse files")

    parser.add_argument("source_dirs")
    parser.add_argument("include_dirs")
    parser.add_argument("output_file")
    parser.add_argument("patch_files")

    args = parser.parse_args()

    source_dirs = [i.strip() for i in args.source_dirs.split()]

    all_sources = []
    for some_dir in source_dirs:
        if some_dir:
            all_sources.extend(find_source(some_dir))

    patch_files = []
    for patch_file in args.patch_files.split():
        temp = os.path.abspath(patch_file)
        patch_files.append(pathlib.Path(temp))
    
    all_sources = [i for i in all_sources if i not in patch_files]

    all_objs = []
    for i in all_sources:
        name, _ = os.path.splitext(os.path.basename(i))
        obj = os.path.join('$(MOCK_OUTPUT)', name + '.o')
        all_objs.append(obj)

    patch_sources = []
    patch_targets = []
    for i in patch_files:
        name, _ = os.path.splitext(os.path.basename(i))
        src = os.path.join('$(MOCK_OUTPUT)', name + '.patch.c')
        obj = os.path.join('$(MOCK_OUTPUT)', name + '.patch.o')

        patch_sources.append(i)
        patch_targets.append(src)

        all_sources.append(src)
        all_objs.append(obj)

    include_dirs = ['-I{}'.format(i.strip()) for i in args.include_dirs.split()]
    includes = ' '.join(include_dirs)

    output_path = os.path.join(args.output_file)
    write_mk(output_path,
            includes,
            all_sources,
            all_objs,
            patch_sources,
            patch_targets)

if __name__== "__main__":
    main()
