import hashlib
import re
import sys
import typing
import yaml
import zipfile

ARCHIVE_REGEX = re.compile(r".*\.(jar|war|ear|zip)$")


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
            if ARCHIVE_REGEX.match(f, re.IGNORECASE):
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


def _compare_archive_data(data1: dict, data2: dict, outfile: typing.TextIO) -> set[str]:
    all_keys = set(data1.keys())
    all_keys.update(data2.keys())

    modified_nested_archives = set()

    for file_path in sorted(list(all_keys)):
        d1 = data1.get(file_path)
        if d1 is None:
            print(f"ADDED,{file_path},,", file=outfile)
            continue

        d2 = data2.get(file_path)
        if d2 is None:
            print(f"REMOVED,{file_path},,", file=outfile)
            continue

        if d1["sha256"] != d2["sha256"] or d1["size"] != d2["size"]:
            print(f"MODIFIED,{file_path},{d1['size']},{d2['size']}", file=outfile)
            if ARCHIVE_REGEX.match(file_path, re.IGNORECASE):
                modified_nested_archives.add(file_path)

    return modified_nested_archives


def _compare_full_data_dict(info_dict_1, info_dict_2, outfile: typing.TextIO):
    modified_archives = _compare_archive_data(
        info_dict_1["root"], info_dict_2["root"], outfile
    )
    for archive_path in modified_archives:
        print(f"\nInspecting modified sub-archive: {archive_path}\n", file=outfile)
        _compare_archive_data(
            info_dict_1["nested"][archive_path],
            info_dict_2["nested"][archive_path],
            outfile,
        )


def compare_files(filename_1: str, filename_2: str):
    data_1 = open_old_data_or_archive(filename_1)
    data_2 = open_old_data_or_archive(filename_2)

    return _compare_full_data_dict(data_1, data_2, sys.stdout)


def eprint(msg, **kwargs):
    print(msg, file=sys.stderr, **kwargs)
