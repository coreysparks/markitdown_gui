# MarkItDown GUI

A small desktop app that puts a graphical front end on Microsoft's
[markitdown](https://github.com/microsoft/markitdown) library. Pick a file, pick
where to save it, click **Convert**, and you get a Markdown file.

The interface is built with `tkinter`, which ships with Python, so the only real
dependency is `markitdown` itself.

## Features

- File pickers for the input document and the output `.md` file
- Output path is suggested automatically from the input file name
- Conversion runs on a background thread, so the window stays responsive
- A status log plus dialog boxes reporting success or the exact error

## Requirements

- Python 3.10 or newer (with `tkinter` — included in the standard Windows and
  macOS installers; on Debian/Ubuntu install `python3-tk`)
- The `markitdown` package

```
pip install "markitdown[all]"
```

The extras control which formats are supported. If you only need a few, install
just those, for example:

```
pip install "markitdown[pdf,docx,pptx,xlsx,xls,outlook]"
```

## Running it

```
python markitdown_gui.py
```

On Windows you can double-click `run_markitdown_gui.bat` instead. That script
checks that Python and `markitdown` are available, offers to install
`markitdown` from a local checkout if it is missing, and then launches the app.

> Note: the local-install fallback in the `.bat` file points at
> `C:\Users\ozd504\markitdown`. Edit those paths if your copy lives elsewhere,
> or delete that block if you installed `markitdown` from PyPI.

## Using it

1. **Browse** to the file you want to convert.
2. Adjust the suggested output path, or use **Save as** to choose another.
3. Click **Convert**.
4. The status box reports where the Markdown file was written, or what went
   wrong.

## Supported formats

Whatever the installed `markitdown` build supports — typically PDF, Word,
PowerPoint, Excel, HTML, CSV, JSON, XML, plain text, Outlook messages, and ZIP
archives. The file picker defaults to those extensions but has an "All files"
option, so you can hand any file to the converter and see what it makes of it.

## Files

| File | Purpose |
| --- | --- |
| `markitdown_gui.py` | The application |
| `run_markitdown_gui.bat` | Windows launcher with dependency checks |

## License

This is a thin wrapper around `markitdown`; see that project for its own
license terms.
