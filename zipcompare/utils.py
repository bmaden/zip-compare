import hashlib
import re
import sys
import typing
import yaml
import zipfile


def traverse(zipfile_name: typing.BinaryIO) -> typing.Dict[str, str]:
    data = dict()
    with zipfile.ZipFile(zipfile_name, "r") as zip_data:
        for info in zip_data.infolist():
            if info.is_dir() is False:
                hasher = hashlib.new("sha256")
                hasher.update(zip_data.read(info.filename))
                data[info.filename] = hasher.hexdigest()

    return data


def traverse_archive(zipfile_name: str) -> dict:
    with open(zipfile_name, "rb") as zip_open:
        file_meta = dict(root=traverse(zip_open), nested=dict())

    with zipfile.ZipFile(zipfile_name, "r") as zip_data:
        for f in file_meta["root"].keys():
            if re.match(r".*\.(jar|war|ear|zip)$", f, re.IGNORECASE):
                with zip_data.open(f, "r") as internal_archive:
                    file_meta["nested"][f] = traverse(internal_archive)

    return file_meta


def compare(infodict1, infodict2):
    pass


def load_previous_data(filename: str) -> dict:
    with open(filename, "r") as data_file:
        data = yaml.full_load(data_file)
    return data


def eprint(msg, **kwargs):
    print(msg, file=sys.stderr, **kwargs)
