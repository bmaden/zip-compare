import argparse

from .utils import eprint, traverse_archive


parser = argparse.ArgumentParser(description="ZIP comparisons")
parser.add_argument("-i", "--inspect-only", dest="inspect_only", action="store_true")
parser.set_defaults(inspect_only=False)
parser.add_argument("files", nargs=argparse.REMAINDER)

args = parser.parse_args()

if args.inspect_only is True:
    if len(args.files) != 1:
        eprint("inspect requires exactly one file")
        exit(1)

    traverse_archive(args.files[0])
