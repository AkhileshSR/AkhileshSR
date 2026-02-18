
#!/usr/bin/env python3
"""
Disk Usage Report
-----------------
Generate a quick summary of a directory tree:
- Total size per top-level child
- Top N largest files
- Optional CSV and Markdown reports

Example:
    python disk_usage_report.py --root . --top 20 --csv report.csv --md report.md
"""
from pathlib import Path
import argparse
import csv


def human_bytes(n: int) -> str:
    for unit in ['B','KB','MB','GB','TB']:
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} PB"


def dir_size(p: Path) -> int:
    total = 0
    for f in p.rglob('*'):
        try:
            if f.is_file():
                total += f.stat().st_size
        except Exception:
            pass
    return total


def top_n_files(root: Path, n: int):
    files = []
    for f in root.rglob('*'):
        try:
            if f.is_file():
                files.append((f.stat().st_size, f))
        except Exception:
            pass
    files.sort(reverse=True, key=lambda x: x[0])
    return files[:n]


def main():
    ap = argparse.ArgumentParser(description='Create a disk usage summary and largest files list.')
    ap.add_argument('--root', type=Path, required=True, help='Root directory to analyze')
    ap.add_argument('--top', type=int, default=10, help='Top N largest files to list')
    ap.add_argument('--csv', type=Path, help='CSV path for largest files report')
    ap.add_argument('--md', type=Path, help='Markdown path for full report')
    args = ap.parse_args()

    root = args.root.expanduser().resolve()
    assert root.exists(), f"Root not found: {root}"

    # Per top-level child size
    child_sizes = []
    for child in root.iterdir():
        if child.is_dir():
            s = dir_size(child)
            child_sizes.append((child.name, s))

    largest = top_n_files(root, args.top)

    # Print summary to console
    print("Top-level directory sizes:")
    for name, s in sorted(child_sizes, key=lambda x: x[1], reverse=True):
        print(f" - {name}: {human_bytes(s)}")
    print("
Largest files:")
    for sz, f in largest:
        print(f" - {f} ({human_bytes(sz)})")

    # Optional CSV
    if args.csv:
        with args.csv.open('w', newline='', encoding='utf-8') as fo:
            w = csv.writer(fo)
            w.writerow(['size_bytes', 'size_human', 'path'])
            for sz, f in largest:
                w.writerow([sz, human_bytes(sz), str(f)])
        print(f"[OK] Wrote CSV: {args.csv}")

    # Optional Markdown
    if args.md:
        lines = ["# Disk Usage Report

", "## Top-level directory sizes

"]
        for name, s in sorted(child_sizes, key=lambda x: x[1], reverse=True):
            lines.append(f"- **{name}**: {human_bytes(s)}
")
        lines.append("
## Largest files

")
        for sz, f in largest:
            lines.append(f"- `{f}` — {human_bytes(sz)}
")
        args.md.write_text(''.join(lines), encoding='utf-8')
        print(f"[OK] Wrote Markdown: {args.md}")

if __name__ == '__main__':
    main()
