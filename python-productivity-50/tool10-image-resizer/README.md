
# Image Resizer (Bulk)

Resize/optimize images to a maximum size and JPEG quality.

## Install
```
pip install Pillow
```

## Usage
```bash
python image_resizer.py --src ./in --out ./out --max-width 1600 --max-height 1200 --quality 85
```

## Notes
- Preserves aspect ratio using `thumbnail`.
- Supports: JPG, PNG, WEBP.
