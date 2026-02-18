
#!/usr/bin/env python3
"""
Folder Organizer
----------------
Sort files in a directory by either **extension** or **modified date**.

- Safe by default (no overwrite). Use --dry-run to simulate.
- Cross-platform (Pathlib) and heavily commented for clarity.

Usage examples:
    python folder_organizer.py --src C:\Downloads --mode extension --dry-run
    python folder_organizer.py --src /tmp/inbox --mode date --copy --dest /tmp/sorted
"""
from pathlib import Path
import shutil
import argparse
from datetime import datetime


def organize_by_extension(src: Path, dest: Path, copy: bool, dry_run: bool):
    """Group files into subfolders named by file extension (e.g., 'pdf', 'jpg')."""
    for p in src.iterdir():
        if p.is_file():
            ext = p.suffix.lower().lstrip('.') or 'no_ext'
            target_dir = dest / ext
            target_dir.mkdir(parents=True, exist_ok=True)
            target_path = target_dir / p.name
            if dry_run:
                print(f"[DRY] {'COPY' if copy else 'MOVE'} {p} -> {target_path}")
            else:
                if copy:
                    shutil.copy2(p, target_path)
                else:
                    shutil.move(str(p), str(target_path))


def organize_by_date(src: Path, dest: Path, copy: bool, dry_run: bool):
    """Group files into subfolders by modified date: YYYY/MM."""
    for p in src.iterdir():
        if p.is_file():
            ts = datetime.fromtimestamp(p.stat().st_mtime)
            year = ts.strftime('%Y')
            month = ts.strftime('%m')
            target_dir = dest / year / month
            target_dir.mkdir(parents=True, exist_ok=True)
            target_path = target_dir / p.name
            if dry_run:
                print(f"[DRY] {'COPY' if copy else 'MOVE'} {p} -> {target_path}")
            else:
                if copy:
                    shutil.copy2(p, target_path)
                else:
                    shutil.move(str(p), str(target_path))


def main():
    parser = argparse.ArgumentParser(description='Organize files by extension or date.')
    parser.add_argument('--src', required=True, type=Path, help='Source directory to scan')
    parser.add_argument('--dest', type=Path, help='Destination directory (defaults to src)')
    parser.add_argument('--mode', choices=['extension', 'date'], required=True, help='Grouping mode')
    parser.add_argument('--copy', action='store_true', help='Copy instead of move')
    parser.add_argument('--dry-run', action='store_true', help='Show actions without changing anything')
    args = parser.parse_args()

    src = args.src.expanduser().resolve()
    dest = (args.dest or src).expanduser().resolve()
    assert src.exists() and src.is_dir(), f"Source does not exist or is not a directory: {src}"
    dest.mkdir(parents=True, exist_ok=True)

    if args.mode == 'extension':
        organize_by_extension(src, dest, args.copy, args.dry_run)
    else:
        organize_by_date(src, dest, args.copy, args.dry_run)

if __name__ == '__main__':
    main()
