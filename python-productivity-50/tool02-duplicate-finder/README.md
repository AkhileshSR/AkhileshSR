
# Duplicate Finder

Find duplicate files by computing content hashes (md5/sha1/sha256). Optionally delete duplicates.

## Usage
```bash
# Report only
python duplicate_finder.py --root ./data --algo sha256 --report dupes.csv

# Delete duplicates (keep newest), dry-run first!
python duplicate_finder.py --root ./data --delete --keep newest --dry-run
python duplicate_finder.py --root ./data --delete --keep newest
```

## Author & License
- Programmer: Akhilesh Singh (AkhileshSR)
- License: MIT — Free to use with credits (see root LICENSE)
