
# Log Summarizer

Scan `*.log` files and count matches for given regex patterns (e.g., `ERROR`, `WARN`). Outputs a console summary and optional Markdown.

## Usage
```bash
python log_summarizer.py --root ./logs --patterns ERROR WARN --out summary.md
```

## Notes
- Uses Python `re` regex; pass multiple patterns.
- Scans recursively from `--root`.
