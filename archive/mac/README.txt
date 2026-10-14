MC PDF Cleaner - macOS Instructions
=====================================

What this does
---------------
Removes the MC_Header, MC_Footer, and MC_Overlay fields from a
MasterControl-published PDF and strips all embedded JavaScript, so the
file displays correctly in any viewer (Preview, Chrome, Adobe Acrobat,
etc.) and ingests as a plain, clean PDF (no leftover MasterControl
boilerplate text or scripts).

Files in this folder
---------------------
- mc_pdf_cleaner.py   The actual cleaning script.
- run.command         Double-click this to run it. Installs the one
                       required library (pymupdf) automatically the
                       first time, then runs the script.

One-time setup
---------------
1. Make run.command executable and remove the macOS quarantine flag
   (needed once, since it wasn't downloaded from the App Store).
   Open Terminal, then run:
       cd /path/to/this/folder
       chmod +x run.command
       xattr -d com.apple.quarantine run.command

2. macOS may still show a warning the first time you double-click it
   ("cannot be opened because it is from an unidentified developer").
   If so: right-click (or Control-click) run.command, choose "Open",
   then click "Open" again in the dialog. You only need to do this once.

Running it
-----------
Option A - Drag and drop:
   Drag a PDF file directly onto run.command in Finder. It will
   process it and create a new file named "<original name>-clean.pdf"
   in the same folder as the input file.

Option B - Terminal:
   cd /path/to/this/folder
   ./run.command "/path/to/input.pdf" "/path/to/output.pdf"
   If you omit the output path, it defaults to "<input>-clean.pdf".

Option C - Double-click with no arguments:
   Double-click run.command directly. It will prompt you to type or
   drag in a file path.

What you'll see
-----------------
The Terminal window will print a short summary, e.g.:
   Removed 8 header field(s), 8 footer field(s), 8 overlay field(s)
   JavaScript-related objects remaining: 0
   SUCCESS: no JavaScript remains in the output file.
   Output written to: ...

Press Enter when prompted to close the window.

Troubleshooting
-----------------
- "python3 was not found": install the Xcode Command Line Tools by
  running "xcode-select --install" in Terminal, then try again.
- "cannot be opened because it is from an unidentified developer":
  see the One-time setup section above.
- pip install fails: check your internet connection.
- Any other error: the full Python error trace will be printed in the
  window - copy it and send it along for help diagnosing it.
