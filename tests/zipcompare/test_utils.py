import pytest
import zipcompare.utils


def test_traverse_archive(resource_path):
    zip_path = resource_path / "test.zip"
    meta = zipcompare.utils.traverse_archive(str(zip_path))

    # directory (doesn't get added to output)
    with pytest.raises(KeyError):
        assert meta["root"]["dir_b/"] == "dir"
    # file in root archive
    assert (
        meta["root"]["dir_a/x/y/z/deep_file.txt"]
        == "98253840c84dd789a6140d2474486fd1d79bc11e92d01ff16d3e5cfbbae92b29"
    )
    # file in nested archive
    assert (
        meta["nested"]["zip/zipped_file.zip"]["dir_y/file_y.txt"]
        == "34e574e523ae82738ba84d2a83c8270f0384976f219527307da5ec3a4b4cc680"
    )
