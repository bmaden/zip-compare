import pathlib
import zipcompare.utils


def test_traversal(resource_path):
    zip_path = resource_path / "test.zip"


    zipcompare.utils.traverse(str(zip_path))


# def test_something2():
#     assert 1 == 2
