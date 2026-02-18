
# Folder Organizer

Sort files by **extension** (pdf, jpg, …) or by **modified date** (YYYY/MM).

## Usage
```bash
# Dry run by extension
python folder_organizer.py --src C:\Users\me\Downloads --mode extension --dry-run

# Move by date into a destination
python folder_organizer.py --src ./inbox --mode date --dest ./sorted

# Copy instead of move
python folder_organizer.py --src ./inbox --mode extension --copy
```

## Notes
- Uses `Pathlib` and is cross-platform.
- `--dry-run` shows what would happen without changing files.
