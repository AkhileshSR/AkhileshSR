#!/usr/bin/env python3
"""
PDF Tool (Merge & Split)
Author : Akhilesh Singh (AkhileshSR)
License: MIT (see LICENSE) — Free to use with attribution.

This script is intentionally **well-commented** to be approachable for
experienced programmers who are newer to Python.
"""

import argparse
from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter

# --- Implementation notes ---------------------------------------------------
# - Merge: concatenates pages from inputs in order.
# - Split: parses 1-based ranges like "1-3,5,7-" into page indices.
# - Writes a single split PDF for selected pages for simplicity.
# ----------------------------------------------------------------------------

def do_merge(output: Path, inputs):
    writer = PdfWriter()
    for f in inputs:
        r = PdfReader(str(f))
        for page in r.pages:
            writer.add_page(page)
    with output.open('wb') as fo:
        writer.write(fo)
    print(f"[OK] Wrote merged PDF: {output}")


def parse_ranges(ranges: str, total_pages: int):
    """Parse a range string like '1-3,5,7-' (1-based) into zero-based indices."""
    result = []
    for part in ranges.split(','):
        part = part.strip()
        if not part:
            continue
        if '-' in part:
            start, end = part.split('-', 1)
            start = int(start) if start else 1
            end = int(end) if end else total_pages
            for p in range(start, end + 1):
                if 1 <= p <= total_pages:
                    result.append(p - 1)
        else:
            p = int(part)
            if 1 <= p <= total_pages:
                result.append(p - 1)
    # Deduplicate while preserving order
    seen = set()
    out = []
    for i in result:
        if i not in seen:
            seen.add(i)
            out.append(i)
    return out


def do_split(src: Path, ranges: str, outdir: Path):
    reader = PdfReader(str(src))
    total = len(reader.pages)
    idxs = parse_ranges(ranges, total)
    outdir.mkdir(parents=True, exist_ok=True)

    w = PdfWriter()
    for i in idxs:
        w.add_page(reader.pages[i])
    out_path = outdir / f"{src.stem}_split.pdf"
    with out_path.open('wb') as fo:
        w.write(fo)
    print(f"[OK] Wrote split PDF: {out_path} (pages: {len(idxs)})")


def main():
    ap = argparse.ArgumentParser(description='Merge or split PDF files.')
    sub = ap.add_subparsers(dest='cmd', required=True)

    m = sub.add_parser('merge', help='Merge PDFs into one')
    m.add_argument('--out', required=True, type=Path, help='Output PDF')
    m.add_argument('inputs', nargs='+', type=Path, help='Input PDFs in order')

    s = sub.add_parser('split', help='Split a PDF by page ranges')
    s.add_argument('--src', required=True, type=Path, help='Source PDF')
    s.add_argument('--ranges', required=True, type=str, help='Ranges like "1-3,5,7-" (1-based)')
    s.add_argument('--outdir', required=True, type=Path, help='Output directory')

    args = ap.parse_args()

    if args.cmd == 'merge':
        do_merge(args.out.expanduser().resolve(), [p.expanduser().resolve() for p in args.inputs])
    else:
        do_split(args.src.expanduser().resolve(), args.ranges, args.outdir.expanduser().resolve())

if __name__ == '__main__':
    main()

