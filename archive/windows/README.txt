MC PDF Cleaner - Windows Instructions
======================================

What this does
---------------
Removes the MC_Header, MC_Footer, and MC_Overlay fields from a
MasterControl-published PDF and strips all embedded JavaScript, so the
file displays correctly in any viewer and ingests as a plain, clean
PDF (no leftover MasterControl boilerplate text or scripts).

Files in this folder
---------------------
- mc_pdf_cleaner.py   The actual cleaning script.
- run.bat             Double-click this to run it. Installs the one
                       required library (pymupdf) automatically the
                       first time, then runs the script.

One-time setup
---------------
1. Install Python 3.11 or newer from https://python.org
   - During installation, check the box that says
     "Add python.exe to PATH" - this is important, don't skip it.
2. That's it. No other software is required.

Running it
-----------
Option A - Drag and drop:
   Drag a PDF file directly onto run.bat. It will process it and
   create a new file named "<original name>-clean.pdf" in the same
   folder as the input file.

Option B - Command line:
   Open Command Prompt in this folder and run:
       run.bat "C:\path\to\input.pdf" "C:\path\to\output.pdf"
   If you omit the output path, it defaults to "<input>-clean.pdf".

Option C - Double-click with no arguments:
   Double-click run.bat directly. It will prompt you to type or
   drag in a file path.

What you'll see
-----------------
The window will print a short summary, e.g.:
   Removed 8 header field(s), 8 footer field(s), 8 overlay field(s)
   JavaScript-related objects remaining: 0
   SUCCESS: no JavaScript remains in the output file.
   Output written to: ...

Press Enter when prompted to close the window.

Troubleshooting
-----------------
- "Python was not found on PATH": reinstall Python and make sure to
  check "Add python.exe to PATH" during setup.
- pip install fails: check your internet connection, or that your
  network/proxy allows pip to reach pypi.org.
- Any other error: the full Python error trace will be printed in the
  window - copy it and send it along for help diagnosing it.
