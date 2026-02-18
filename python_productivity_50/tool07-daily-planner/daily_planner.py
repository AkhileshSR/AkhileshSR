#!/usr/bin/env python3
"""
Daily Planner Generator (Markdown)
Author : Akhilesh Singh (AkhileshSR)
License: MIT (see LICENSE) — Free to use with attribution.

This script is intentionally **well-commented** to be approachable for
experienced programmers who are newer to Python.
"""

from pathlib import Path
import argparse
from datetime import datetime

# --- Implementation notes ---------------------------------------------------
# - Generates an opinionated Markdown day plan with time blocks.
# - The filename embeds the ISO date for easy sorting.
# ----------------------------------------------------------------------------

TEMPLATE = """# Daily Planner — {date_human}

## Top 3 Priorities
- [ ] 
- [ ] 
- [ ] 

## Time-blocks
| Time | Task |
|------|------|
| 09:00 |  |
| 10:00 |  |
| 11:00 |  |
| 12:00 |  |
| 13:00 |  |
| 14:00 |  |
| 15:00 |  |
| 16:00 |  |
| 17:00 |  |

## Tasks / Notes
- 

## Reflection
- What went well?
- What can be improved tomorrow?
"""

def main():
    ap = argparse.ArgumentParser(description='Generate a Markdown daily planner file.')
    ap.add_argument('--date', type=str, help='YYYY-MM-DD (defaults to today)')
    ap.add_argument('--out', type=Path, required=True, help='Output directory')
    args = ap.parse_args()

    if args.date:
        dt = datetime.strptime(args.date, '%Y-%m-%d').date()
    else:
        dt = datetime.today().date()

    date_human = dt.strftime('%A, %d %B %Y')
    content = TEMPLATE.format(date_human=date_human)

    outdir = args.out.expanduser().resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    outpath = outdir / f"planner_{dt.isoformat()}.md"
    outpath.write_text(content, encoding='utf-8')
    print(f"[OK] Wrote planner: {outpath}")

if __name__ == '__main__':
    main()

