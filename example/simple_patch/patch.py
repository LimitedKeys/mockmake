
import argparse

def main(path, out):
    with open(path, 'r') as in_file:
        lines = in_file.readlines()

    # Parse lines here

    with open(out, 'w') as out_file:
        out_file.writelines(lines)

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Patch")
    parser.add_argument("path", 
            help="File to be patched")
    parser.add_argument("output",
            help="Patched file path")

    args = parser.parse_args()

    main(args.path, args.output)
