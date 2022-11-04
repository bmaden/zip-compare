import re
import sys
import typing
import zipfile


def traverse(zipfile_name: str) -> typing.Dict[str, typing.List[zipfile.ZipInfo]]:
    with zipfile.ZipFile(zipfile_name, "r") as zipdata:
        return {info.filename: info.CRC for info in zipdata.infolist()}


def traverse_archive(zipfile_name: str) -> dict:
    file_meta = dict(root=traverse(zipfile_name), nested=dict())

    for f in file_meta["root"].keys():
        print(f"testing: {f}")
        if re.match(r".*\.(jar|war|ear|zip)$", f, re.IGNORECASE):
            print(f"extracting: {f}")
            z = zipfile.ZipFile(zipfile_name)
            f_open = z.open(f)
            file_meta["nested"][f] = traverse(f_open)

    return file_meta


def compare(infodict1, infodict2):
    pass


def eprint(msg, **kwargs):
    print(msg, file=sys.stderr, **kwargs)
