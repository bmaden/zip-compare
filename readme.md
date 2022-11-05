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
