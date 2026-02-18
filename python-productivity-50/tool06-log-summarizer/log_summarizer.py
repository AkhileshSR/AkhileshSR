
#!/usr/bin/env python3
"""
Log Summarizer
--------------
Scan .log files, extract lines matching regex (e.g., ERROR|WARN), and produce a summary count per pattern.

Example:
    python log_summarizer.py --root ./logs --patterns ERROR WARN --out summary.md
"""
from pathlib import Path
import argparse
import re
from collections import Counter


def summarize_logs(root: Path, patterns):
    counters = {p: Counter() for p in patterns}
    regexes = {p: re.compile(p) for p in patterns}

    for f in root.rglob('*.log'):
        try:
            for line in f.read_text(errors='ignore').splitlines():
                for p, rx in regexes.items():
                    if rx.search(line):
                        counters[p][f.name] += 1
        except Exception as e:
            print(f"[WARN] Failed to read {f}: {e}")

    return counters


def write_markdown(counters, out_md: Path):
    lines = ["# Log Summary

"]
    for pat, counter in counters.items():
        lines.append(f"## Pattern: `{pat}`

")
        total = sum(counter.values())
        lines.append(f"Total matches: **{total}**

")
        for fname, cnt in counter.most_common():
            lines.append(f"- {fname}: {cnt}
")
        lines.append("
")
    out_md.write_text(''.join(lines), encoding='utf-8')


def main():
    ap = argparse.ArgumentParser(description='Summarize log files by regex patterns.')
    ap.add_argument('--root', type=Path, required=True, help='Root folder to scan (recursively)')
    ap.add_argument('--patterns', nargs='+', required=True, help='Regex patterns to search for (e.g., ERROR WARN)')
    ap.add_argument('--out', type=Path, help='Write summary to Markdown file')
    args = ap.parse_args()

    root = args.root.expanduser().resolve()
    assert root.exists(), f"Root not found: {root}"

    counters = summarize_logs(root, args.patterns)

    # Console output
    for pat, counter in counters.items():
        total = sum(counter.values())
        print(f"Pattern '{pat}': total matches = {total}")
        for fname, cnt in counter.most_common()[:10]:
            print(f"  - {fname}: {cnt}")

    if args.out:
        write_markdown(counters, args.out.expanduser().resolve())
        print(f"[OK] Wrote {args.out}")

if __name__ == '__main__':
    main()
