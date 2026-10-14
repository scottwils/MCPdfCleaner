# MCPdfCleaner

Removes the **MC_Header**, **MC_Footer**, and **MC_Overlay** form fields entirely
(so no MasterControl boilerplate text remains on the page for clean downstream
ingestion) and strips embedded JavaScript from the PDF so it displays correctly
in any viewer (Preview, Chrome, Adobe Acrobat, etc.) without needing a
JS-capable reader.

## Usage

```
python mc_pdf_cleaner.py input.pdf [output.pdf]
```

Drag a PDF onto the script (or call with no args) and it prompts for a path.
If a second argument is given, that's the output path; otherwise it writes
`<input>-clean.pdf` next to the input.

## Building the Windows .exe

This repo runs a GitHub Actions workflow on every pushed tag and on a manual
"Run workflow" button click. It produces a single self-contained
`MCPdfCleaner.exe` and uploads it as a downloadable artifact — **no
Python installation required to run the .exe**, on any Windows 11 machine.

### Get the latest .exe without doing a release

1. Click the **Actions** tab at https://github.com/scottwils/MCPdfCleaner
2. Open the most recent "Build Windows .exe" workflow run
3. Scroll to the bottom — under **Artifacts**, download `MCPdfCleaner-windows`
4. Unzip → inside you'll find `MCPdfCleaner.exe`
5. Copy that single file to any Windows 11 PC. Drag PDFs onto it, or run
   `MCPdfCleaner.exe input.pdf output.pdf` from Command Prompt.

### Run it on macOS / Linux (dev use)

```
pip install pymupdf
python mc_pdf_cleaner.py some.pdf
```

## Requirements

- PyMuPDF (`pip install pymupdf`)

That's it. No external command-line tools, no Adobe dependency, no viewer
interactions.
