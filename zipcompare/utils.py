import sys
import typing
import zipfile


def traverse(zipfile_name: str) -> typing.Dict[str, typing.List[zipfile.ZipInfo]]:
    with zipfile.ZipFile(zipfile_name, "r") as zipdata:
        return {info.filename: info for info in zipdata.infolist()}


def traverse_archive(zipfile_name: str) -> dict:
    file_meta = dict(root=traverse(zipfile_name), nested=dict())
    return file_meta


def compare(infodict1, infodict2):
    pass


def eprint(msg, **kwargs):
    print(msg, file=sys.stderr, **kwargs)
