#!/usr/bin/env python3
"""
Image Resizer (Bulk)
Author : Akhilesh Singh (AkhileshSR)
License: MIT (see LICENSE) — Free to use with attribution.

This script is intentionally **well-commented** to be approachable for
experienced programmers who are newer to Python.
"""

from pathlib import Path
import argparse
from PIL import Image

# --- Implementation notes ---------------------------------------------------
# - Uses Pillow's thumbnail() to preserve aspect ratio within a max box.
# - Applies JPEG quality settings and optimize flag for JPG/JPEG.
# ----------------------------------------------------------------------------

SUPPORTED = {'.jpg', '.jpeg', '.png', '.webp'}


def process(src: Path, out: Path, max_w: int, max_h: int, quality: int):
    out.mkdir(parents=True, exist_ok=True)
    for p in src.iterdir():
        if p.is_file() and p.suffix.lower() in SUPPORTED:
            im = Image.open(p)
            im.thumbnail((max_w, max_h))  # in-place resize preserving aspect ratio
            target = out / p.name
            save_args = {}
            if target.suffix.lower() in {'.jpg', '.jpeg'}:
                save_args.update({'optimize': True, 'quality': quality})
            im.save(target, **save_args)
            print(f"[OK] {p.name} -> {target} ({im.width}x{im.height})")


def main():
    ap = argparse.ArgumentParser(description='Bulk image resizer for JPG/PNG/WEBP.')
    ap.add_argument('--src', type=Path, required=True, help='Input folder')
    ap.add_argument('--out', type=Path, required=True, help='Output folder')
    ap.add_argument('--max-width', type=int, default=1600)
    ap.add_argument('--max-height', type=int, default=1200)
    ap.add_argument('--quality', type=int, default=85, help='JPEG quality (1-95)')
    args = ap.parse_args()

    process(args.src.expanduser().resolve(), args.out.expanduser().resolve(), args.max_width, args.max_height, args.quality)



if __name__ == '__main__':
    main()

