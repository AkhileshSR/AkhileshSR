
#!/usr/bin/env python3
"""
Smart Renamer
-------------
Batch rename files with prefix/suffix and sequence numbers.
Supports preview mode and filtering by extension.

Example:
    python smart_renamer.py --dir ./images --prefix trip_ --ext .jpg --seq --dry-run
    python smart_renamer.py --dir ./docs --suffix _final --ext .pdf
"""
from pathlib import Path
import argparse


def smart_rename(dir_path: Path, prefix: str, suffix: str, ext_filter: str, seq: bool, start: int, dry: bool):
    files = [p for p in dir_path.iterdir() if p.is_file() and (not ext_filter or p.suffix.lower() == ext_filter.lower())]
    files.sort()
    counter = start
    for p in files:
        stem = p.stem
        new_stem = f"{prefix or ''}{stem}{suffix or ''}"
        if seq:
            new_stem = f"{new_stem}_{counter:03d}"
            counter += 1
        new_name = new_stem + p.suffix
        target = p.with_name(new_name)
        if dry:
            print(f"[PREVIEW] {p.name} -> {target.name}")
        else:
            p.rename(target)
            print(f"[OK] {p.name} -> {target.name}")


def main():
    ap = argparse.ArgumentParser(description='Batch rename files with prefix/suffix and optional sequence numbers.')
    ap.add_argument('--dir', type=Path, required=True, help='Directory containing files')
    ap.add_argument('--prefix', type=str, default='', help='Prefix to add')
    ap.add_argument('--suffix', type=str, default='', help='Suffix to add')
    ap.add_argument('--ext', type=str, default='', help='Filter by extension (e.g., .jpg)')
    ap.add_argument('--seq', action='store_true', help='Append sequence numbers')
    ap.add_argument('--start', type=int, default=1, help='Sequence start value')
    ap.add_argument('--dry-run', action='store_true', help='Preview without renaming')
    args = ap.parse_args()

    d = args.dir.expanduser().resolve()
    assert d.exists() and d.is_dir(), f"Directory not found: {d}"

    smart_rename(d, args.prefix, args.suffix, args.ext, args.seq, args.start, args.dry_run)

if __name__ == '__main__':
    main()
