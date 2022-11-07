import hashlib
import re
import sys
import typing
import yaml
import zipfile


def traverse(zipfile_name: typing.BinaryIO) -> typing.Dict[str, dict[str | int]]:
    data = dict()
    with zipfile.ZipFile(zipfile_name, "r") as zip_data:
        for info in zip_data.infolist():
            if info.is_dir() is False:
                hasher = hashlib.new("sha256")
                hasher.update(zip_data.read(info.filename))
                data[info.filename] = {
                    "sha256": hasher.hexdigest(),
                    "size": info.file_size,
                }

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


def load_previous_data(filename: str) -> dict:
    with open(filename, "r") as data_file:
        return yaml.full_load(data_file)


def open_old_data_or_archive(filename: str):
    if re.match(r".*\.ya?ml$", filename, re.IGNORECASE):
        return load_previous_data(filename)
    else:
        return traverse_archive(filename)


def compare(info_dict_1, info_dict_2):
    print("compare")
    print(info_dict_1)
    print(info_dict_2)


def compare_files(filename_1: str, filename_2: str):
    data_1 = open_old_data_or_archive(filename_1)
    data_2 = open_old_data_or_archive(filename_2)

    return compare(data_1, data_2)


def eprint(msg, **kwargs):
    print(msg, file=sys.stderr, **kwargs)
