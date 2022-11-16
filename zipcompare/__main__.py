import argparse
import sys
import yaml

from .utils import compare_files, eprint, traverse_archive


parser = argparse.ArgumentParser(prog="zipcompare", description="ZIP comparisons")
parser.add_argument("-o", "--output", dest="output_file")
parser.add_argument("-i", "--inspect-only", dest="inspect_only", action="store_true")
parser.set_defaults(inspect_only=False)
parser.add_argument("files", nargs=argparse.REMAINDER)

args = parser.parse_args()

out_file_open = sys.stdout if args.output_file is None else open(args.output_file, "w")

if args.inspect_only is True:
    if len(args.files) != 1:
        eprint("inspect requires exactly one file")
        exit(1)

    info = traverse_archive(args.files[0])
    yaml.dump(info, out_file_open)
elif len(args.files) == 2:
    compare_files(*args.files, outfile=out_file_open)
else:
    parser.print_help()
