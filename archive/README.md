End-user launcher scripts for people who'd rather not touch a terminal.

- `archive/mac/run.command` — double-clickable macOS launcher
- `archive/mac/README.txt` — user-facing instructions for the mac launcher
- `archive/windows/run.bat` — Windows batch launcher (auto-installs PyMuPDF on first run)
- `archive/windows/README.txt` — user-facing instructions for the Windows batch launcher
- `archive/mac/mc_pdf_cleaner.py` and `archive/windows/mc_pdf_cleaner.py` — snapshots of the script
  at the time these were packaged, left here as historical reference. The current version
  of the script is at the repo root: `../mc_pdf_cleaner.py`.

If you're distributing this tool inside an organization, hand a colleague either:

1. The built `MCPdfCleaner.exe` artifact (no install required), or
2. This `archive/mac/` or `archive/windows/` folder (rebuild-or-install required).

**Don't** hand them the bare `mc_pdf_cleaner.py` — without a wrapper they'd need to
open Terminal / Command Prompt themselves.
