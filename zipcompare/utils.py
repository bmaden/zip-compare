import hashlib
import re
import sys
import typing
import zipfile


def traverse(zipfile_name: typing.BinaryIO) -> typing.Dict[str, str]:
    data = dict()
    with zipfile.ZipFile(zipfile_name, "r") as zipdata:
        for info in zipdata.infolist():
            if info.is_dir() is False:
                hasher = hashlib.new("sha256")
                hasher.update(zipdata.read(info.filename))
                data[info.filename] = hasher.hexdigest()

    return data


def traverse_archive(zipfile_name: str) -> dict:
    with open(zipfile_name, "rb") as zip_open:
        file_meta = dict(root=traverse(zip_open), nested=dict())

    with zipfile.ZipFile(zipfile_name, "r") as zipdata:
        for f in file_meta["root"].keys():
            if re.match(r".*\.(jar|war|ear|zip)$", f, re.IGNORECASE):
                with zipdata.open(f) as internal_archive:
                    file_meta["nested"][f] = traverse(internal_archive)

    return file_meta


def compare(infodict1, infodict2):
    pass


def eprint(msg, **kwargs):
    print(msg, file=sys.stderr, **kwargs)
