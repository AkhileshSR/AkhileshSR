
#!/usr/bin/env python3
"""
Duplicate Finder
----------------
Recursively scan a directory, compute file hashes, and report duplicates.
Optionally delete duplicates, keeping the newest or the first occurrence.

Example:
    python duplicate_finder.py --root ./data --algo sha256 --report dupes.csv
    python duplicate_finder.py --root ./data --delete --keep newest
"""
from pathlib import Path
import hashlib
import argparse
import csv
from collections import defaultdict


def file_hash(path: Path, algo: str = 'sha256', chunk_size: int = 1<<20) -> str:
    """Compute a hash for a file using buffered reads to support large files."""
    h = getattr(hashlib, algo)()
    with path.open('rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def scan(root: Path, algo: str):
    """Return dict: hash -> list[Path]."""
    mapping = defaultdict(list)
    for p in root.rglob('*'):
        if p.is_file():
            try:
                h = file_hash(p, algo)
                mapping[h].append(p)
            except Exception as e:
                print(f"[WARN] Cannot hash {p}: {e}")
    return mapping


def write_report(mapping, out_csv: Path):
    with out_csv.open('w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['hash', 'path'])
        for h, paths in mapping.items():
            if len(paths) > 1:
                for p in paths:
                    w.writerow([h, str(p)])


def delete_duplicates(mapping, keep: str, dry_run: bool):
    """Delete duplicates per hash, keeping one file as specified by `keep`.

    keep: 'first' (lexicographic) or 'newest' (by mtime)
    """
    for h, paths in mapping.items():
        if len(paths) <= 1:
            continue
        if keep == 'first':
            survivor = sorted(paths, key=lambda p: str(p))[0]
        else:
            survivor = sorted(paths, key=lambda p: p.stat().st_mtime, reverse=True)[0]
        for p in paths:
            if p == survivor:
                continue
            if dry_run:
                print(f"[DRY] DELETE duplicate: {p}")
            else:
                try:
                    p.unlink()
                    print(f"[OK] Deleted duplicate: {p}")
                except Exception as e:
                    print(f"[ERR] Failed to delete {p}: {e}")


def main():
    ap = argparse.ArgumentParser(description='Find and optionally delete duplicate files by content hash.')
    ap.add_argument('--root', type=Path, required=True, help='Root directory to scan')
    ap.add_argument('--algo', choices=['md5', 'sha1', 'sha256'], default='sha256', help='Hash algorithm')
    ap.add_argument('--report', type=Path, help='CSV report path (optional)')
    ap.add_argument('--delete', action='store_true', help='Delete duplicates (dangerous)')
    ap.add_argument('--keep', choices=['first', 'newest'], default='newest', help='Which file to keep among duplicates')
    ap.add_argument('--dry-run', action='store_true', help='Show what would be deleted')
    args = ap.parse_args()

    root = args.root.expanduser().resolve()
    assert root.exists(), f"Root does not exist: {root}"

    mapping = scan(root, args.algo)
    dupes = {h: p for h, p in mapping.items() if len(p) > 1}
    print(f"Found {len(dupes)} duplicate groups.")

    if args.report:
        write_report(mapping, args.report.expanduser().resolve())
        print(f"Wrote report to {args.report}")

    if args.delete:
        delete_duplicates(mapping, args.keep, args.dry_run)

if __name__ == '__main__':
    main()
