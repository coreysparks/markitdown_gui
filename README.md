# MarkItDown GUI

A small desktop app that puts a graphical front end on Microsoft's
[markitdown](https://github.com/microsoft/markitdown) library. Pick your files,
pick a folder to save them in, click **Convert**, and you get a Markdown file
for each one.

The interface is built with `tkinter`, which ships with Python, so the only real
dependency is `markitdown` itself.

## Features

- Pick any number of input files at once and manage them in a list
- Choose a single output folder; each file is written there as `<name>.md`
- Optional overwrite toggle, so existing Markdown files can be left alone
- Files with the same name from different folders get `_2`, `_3`, … suffixes
  instead of clobbering each other
- Conversion runs on a background thread, so the window stays responsive
- A progress bar plus a per-file status log and a summary of how many files
  converted, were skipped, or failed

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

1. **Add files** to pick one or more documents. You can click **Add files**
   again to append more; **Remove** drops the rows you selected in the list and
   **Clear** empties it.
2. Set the **Output folder**. It defaults to the folder of the first file you
   added, and **Browse** picks another. The folder is created if it does not
   exist yet.
3. Decide whether to leave *Overwrite existing Markdown files* ticked. Unticked,
   any file whose `.md` already exists in the output folder is skipped.
4. Click **Convert**.
5. The progress bar advances per file and the status box lists each conversion,
   skip, or error, followed by a summary.

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
