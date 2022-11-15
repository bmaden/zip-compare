# zip-compare

Some utilities to help compare nested zip archives.  This was created for a specific purpose where the file size, depth of nesting, and number of files was constrained so there wasn't any care taken to minimize open files or memory usage.

## Usage

```bash
python3 -m zipcompare --help
```

### Inspecting one archive

```bash
python3 -m zipcompare -i /path/to/file.zip
```

### Comparing files

Compare two files, these can be either yaml or zip.  The yaml files are the result of the inspect command described above.

```bash
python3 -m zipcompare file1.zip file2.yml
```

## Coverage

```bash
# collect data
coverage run -m pytest

# report
coverage report -m
# (or)
coverage html
```