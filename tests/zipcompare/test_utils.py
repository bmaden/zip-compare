import io
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
        meta["root"]["dir_a/x/y/z/deep_file.txt"]["sha256"]
        == "98253840c84dd789a6140d2474486fd1d79bc11e92d01ff16d3e5cfbbae92b29"
    )
    assert meta["root"]["dir_a/x/y/z/deep_file.txt"]["size"] == 36
    # file in nested archive
    assert (
        meta["nested"]["zip/zipped_file.zip"]["dir_y/file_y.txt"]["sha256"]
        == "34e574e523ae82738ba84d2a83c8270f0384976f219527307da5ec3a4b4cc680"
    )
    assert meta["nested"]["zip/zipped_file.zip"]["dir_y/file_y.txt"]["size"] == 7


def test_load_old_data(resource_path):
    yml_path = resource_path / "test.yml"
    data = zipcompare.utils.load_previous_data(yml_path)
    assert all(k in data.keys() for k in ("root", "nested"))
    assert (
        data["root"]["dir_a/x/y/z/deep_file.txt"]["sha256"]
        == "98253840c84dd789a6140d2474486fd1d79bc11e92d01ff16d3e5cfbbae92b29"
    )
    assert data["root"]["dir_a/x/y/z/deep_file.txt"]["size"] == 36


def test_compare_archive_data():
    data1 = {
        "path1": {"sha256": "hash_00001", "size": 100},
        "path2": {"sha256": "hash_2xxxx", "size": 200},
        "path3": {"sha256": "hash_00003", "size": 300},
        "path4": {"sha256": "hash_00004", "size": 400},
    }
    data2 = {
        "path1": {"sha256": "hash_00001", "size": 100},
        "path2": {"sha256": "hash_00002", "size": 200},
        "path3": {"sha256": "hash_00003", "size": 333},
        "path5": {"sha256": "hash_00005", "size": 500},
    }

    expected_out = [
        "MODIFIED,path2,200,200\n",
        "MODIFIED,path3,300,333\n",
        "REMOVED,path4,,\n",
        "ADDED,path5,,\n",
    ]

    with io.StringIO() as f:
        zipcompare.utils._compare_archive_data(data1, data2, outfile=f)
        f.seek(0)

        for i, line in enumerate(f.readlines()):
            assert line == expected_out[i]
