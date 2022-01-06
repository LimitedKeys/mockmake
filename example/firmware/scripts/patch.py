
import argparse

def main(path, out):
    with open(path, 'r') as in_file:
        lines = in_file.readlines()

    patch = []
    for line in lines:
        if "for(;;) {" in line:
            patch.append("{\n")
        else:
            patch.append(line)

    with open(out, 'w') as out_file:
        out_file.writelines(patch)

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Patch")
    parser.add_argument("path", 
            help="File to be patched")
    parser.add_argument("output",
            help="Patched file path")

    args = parser.parse_args()

    main(args.path, args.output)
