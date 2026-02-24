# pdf-handler

Built to facilitate the extraction and manipulation of content contained in PDF files. To this end, it includes Python utilities to extract relevant content for manipulation using PyMuPDF, such as text, x and y position, RGB color, size, font, etc., and then pre-configured functions to facilitate these manipulations, such as sort content by criterion, join contents from same attribute, etc.

## What this project does

This project parses a PDF into a hierarchy of objects:

- `Page`
- `Block`
- `Line`
- `Content` (text spans)

It also provides `PDFContents`, a list-like container with helpers to:

- sort extracted content by any attribute path
- merge sequential spans into larger text chunks
- assign horizontal buckets (useful for column detection)
- retrieve content from the same row or matching attribute
- validate expected content patterns

## Features

- Extract raw text lines from a PDF (`extract_texts`)
- Extract rich span metadata (`extract_contents`)
- Built-in text cleanup (`_format_text`) for hidden separators, tabs, and repeated spaces
- Optional in-memory caching for extracted texts and contents
- Support for password-protected PDFs when the password is embedded in the filename

## Requirements

- Python 3.10+
- [PyMuPDF (`fitz`)](https://pymupdf.readthedocs.io/)
- `pandas` is only needed if you want to export results to Excel (as shown in `main_test.py`)

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate
pip install pymupdf pandas
```

## Project layout

```text
pdf-handler/
|-- extract/
|   |-- __init__.py    # PDFExtractor
|   `-- contents.py    # Page/Block/Line/Content/PDFContents
|-- main.py            # minimal usage example
|-- main_test.py       # exploratory script + DataFrame/Excel export
`-- README.md
```

## Quick start

```python
from extract import PDFExtractor

pdf_path = r"C:\path\to\file.pdf"
extractor = PDFExtractor(pdf_path)

contents = extractor.extract_contents()
if contents is not None:
    contents.sort()
    contents.join()

    for content in contents[:5]:
        print(content.text, content.xo, content.yo)
else:
    print("No content extracted.")
```

To run the sample entry point:

```bash
python main.py
```

## Password-protected PDFs

If the PDF is encrypted, this project tries to read the password from the filename using the pattern:

```text
anything#PASSWORD#.pdf
```

Example:

```text
statement#mySecret123#.pdf
```

If no password is found in this format, or authentication fails, an exception is raised.

## Core API

### `PDFExtractor`

- `PDFExtractor(pdf_file_path: str | Path)`
- `extract_contents(use_cache: bool = True) -> PDFContents | None`
- `extract_texts(use_cache: bool = True) -> list[str] | None`

### `PDFContents` helpers

- `sort(by=(...), use_cache=True)` / `sorted(...)`
- `join(use_cache=True)` / `joined(...)`
- `assign_horizontal_end_on_page(x_delimiters, use_cache=True)`
- `horizontal_end_on_page_assigned(x_delimiters, use_cache=True)`
- `get_contents_from_same_attr(i_ref, attr, diff_tolerance=0)`
- `get_contents_from_same_row(i_ref, yo_diff_tolerance=0.0)`
- `check_if_matches(known_contents, exactly_text=False)`

## Data model notes

`Content` stores:

- text (`text`)
- bounding box (`xl`, `yt`, `xr`, `yb`)
- origin (`xo`, `yo`)
- dimensions (`width`, `height`, `area`)
- style/flags (`font`, `size`, `rgb_color`, `flags`, etc.)
- parent references (`line`, `block`, `page`)

Each level (`Page`, `Block`, `Line`, `Content`) exposes `get_dict()` to flatten metadata for tabular workflows.

## Example: export to Excel

```python
import pandas as pd
from extract import PDFExtractor

extractor = PDFExtractor(r"C:\path\to\file.pdf")
contents = extractor.extract_contents()

if contents:
    contents.sort()
    contents.join()
    df = pd.DataFrame([content.get_dict() for content in contents])
    df.to_excel("contents.xlsx", index=False)
```

## Notes

- Coordinates come from PyMuPDF and are measured in PDF points.
- Empty/whitespace-only spans are skipped.
- `main_test.py` is a script for manual experimentation; it is not an automated test suite.

## License

MIT. See `LICENSE`.
