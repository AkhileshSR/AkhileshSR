
# PDF Tool (Merge & Split)

Merge multiple PDFs or split selected pages from one PDF.

## Install
```
pip install PyPDF2
```

## Usage
```bash
# Merge (in order)
python pdf_tool.py merge --out merged.pdf file1.pdf file2.pdf

# Split selected pages (1-based ranges)
python pdf_tool.py split --src big.pdf --ranges "1-3,5,7-" --outdir ./splits
```

## Notes
- Ranges are 1-based. `7-` means from page 7 to the end.
- Creates a single output PDF for the specified pages.
