
# Top 10 Python Productivity Tools (Ready for GitHub)

This repository contains **10 practical, beginner-friendly yet professional** productivity tools written in Python. Each tool lives in its own folder with:

- A well‑commented Python script (`.py`)
- A focused `README.md` with usage examples

> Target user: Experienced programmer (25+ years) with <1 year in Python.
>
> Philosophy: Clean CLI design, standard library first, clear comments, and safe defaults.

## Tools Included

1. **Folder Organizer** – Sort files by extension or date
2. **Duplicate Finder** – Find (and optionally delete) duplicate files by hash
3. **Smart Renamer** – Batch rename with prefix/suffix/sequence patterns
4. **PDF Tool** – Merge and split PDFs (ranges)
5. **Disk Usage Report** – Largest files and directory size summary (CSV/MD)
6. **Log Summarizer** – Extract errors/warnings by regex, counts, and report
7. **Daily Planner Generator** – Create a Markdown day planner template
8. **Time Tracker (CLI)** – Start/stop tasks and report totals (CSV backend)
9. **Pomodoro Timer (CLI)** – Focus timer with short/long breaks (console)
10. **Image Resizer** – Bulk resize/compress images (Pillow)

## Quick Start

```bash
python --version  # Python 3.9+

# Create a virtual environment (recommended)
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
# source venv/bin/activate

# (Only two tools need third‑party libs)
pip install -r requirements.txt
```

## Requirements

- Standard library for most tools
- `Pillow` for **Image Resizer**
- `PyPDF2` for **PDF Tool**

```
Pillow>=10.0.0
PyPDF2>=3.0.0
```

## Contributing / Customizing
- Each script is standalone and safe to tweak.
- Most commands support a `--dry-run` or `--preview` mode.

Happy automating! 🚀
