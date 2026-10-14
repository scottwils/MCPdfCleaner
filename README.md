# MCPdfCleaner

**Free, offline tool to extract content from MasterControl-controlled PDFs.**

If you've ever pulled a PDF from MasterControl and found it has a giant
"CONTROLLED COPY" banner stamped across the top, a "DO NOT DUPLICATE"
footer, an expiration watermark, and content that won't copy/paste without
Acrobat Pro — this is for you.

MCPdfCleaner is a small Python script (and a built Windows `.exe` if you
don't want to install Python) that strips all of that:

- **MC_Header** — the orange/red "Controlled Document" banner at the top
- **MC_Footer** — the "This document was printed from MasterControl..." footer
- **MC_Overlay** — per-page watermarks / form overlays
- **Embedded JavaScript** — MasterControl uses `/JS` + `/OpenAction` to
  enforce the watermark and expiration timer; if your PDF viewer doesn't
  execute JS (Chrome, macOS Preview, most mobile viewers) you may see a
  blank page or garbled content. MCPdfCleaner removes this entirely.

Result: a clean, plain PDF you can print, e-mail, archive, OCR, or feed
to any downstream system. No Adobe Acrobat. No MasterControl account.
No internet connection required after installation.

---

## Quick start — Windows (no Python needed)

1. Open the [latest workflow run](../../actions) on the **Actions** tab
2. Scroll to **Artifacts**, download `MCPdfCleaner-windows`
3. Unzip → inside you'll find one file: **`MCPdfCleaner.exe`**
4. Copy it anywhere. Double-click `MCPdfCleaner.exe`, or drag any PDF
   onto it. A new file named `<original>-clean.pdf` appears next to it.

That's it. No installer, no admin rights, no Python, no DLL hell.

## Quick start — macOS / Linux

```bash
pip install pymupdf
python mc_pdf_cleaner.py input.pdf
# Writes input-clean.pdf in the same folder
```

Or drag a PDF onto `mc_pdf_cleaner.py` in Finder and it prompts
interactively for an output path.

## Usage

```
python mc_pdf_cleaner.py <input.pdf> [<output.pdf>]
```

| Argument | Behavior |
|----------|----------|
| Nothing | Prompts for a path; supports drag-and-drop |
| One arg  | Cleans `<input.pdf>` → writes to `<input>-clean.pdf` |
| Two args | `<input.pdf>` → `<output.pdf>` |

## What you'll see

```
Removed 3 header field(s), 3 footer field(s), 3 overlay field(s)
JavaScript-related objects remaining: 0
SUCCESS: no JavaScript remains in the output file.
Output written to: ./input-clean.pdf
```

## Security / privacy notes

- **Runs entirely locally.** No uploads, no telemetry, no analytics.
- The script only reads the PDF you point it at and writes a new file.
- It does **not** crack passwords or bypass encryption. MasterControl
  PDFs are typically *unencrypted* — the visual restrictions are enforced
  via JavaScript and form fields, not crypto. If your PDF has a real
  password, you need the password first; this tool won't guess it.
- The script does not modify, forge, or re-sign any MasterControl audit
  trail. It only removes visual / runtime restrictions on a copy you
  already possess.

## Requirements

- Python 3.11 or newer
- [PyMuPDF](https://pymupdf.readthedocs.io/) — `pip install pymupdf`

## Building the Windows .exe from source

The repo's GitHub Actions workflow (`.github/workflows/build-windows.yml`)
builds a fresh `.exe` automatically on every push to `main` and on every
tagged release. You can also build it yourself:

```cmd
pip install pymupdf pyinstaller
pyinstaller --onefile --console --name MCPdfCleaner mc_pdf_cleaner.py
```

Output: `dist\MCPdfCleaner.exe` — a single self-contained binary you can
ship or copy anywhere.

> PyInstaller is not a cross-compiler. To produce a Windows `.exe` you
> must build on Windows. The CI workflow above runs on a `windows-latest`
> GitHub-hosted runner for exactly this reason.

## Convenience launchers (for end users)

Bundled in `archive/`:

- **`archive/windows/`** — contains `run.bat` (auto-installs PyMuPDF on
  first run, then runs the script) and the version-specific README for
  handing to users who can't fetch the `.exe` artifact.
- **`archive/mac/`** — contains `run.command` (double-clickable macOS
  launcher) plus the matching README.

These are convenience wrappers for letting less-technical colleagues
run the script without touching a terminal.

## License

MIT. Use it, fork it, ship it internally, whatever.

## Tested on

- MasterControl Training PDFs (course/quiz packets)
- MasterControl Change Request Forms (CRF-* document IDs)
- MasterControl "View-only" link downloads
- MasterControl Audit Reports

If you find one it doesn't clean correctly, open an issue with a sample
(redact any confidential headers/footers first) and I'll update the
field-detection list.
