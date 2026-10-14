#!/usr/bin/env python3
"""
MasterControl PDF Cleaner
--------------------------
Removes the MC_Header, MC_Footer, and MC_Overlay form fields entirely
(so no MasterControl boilerplate text remains on the page for clean
downstream ingestion) and strips embedded JavaScript from the PDF so
it displays correctly in any viewer (Preview, Chrome, Adobe Acrobat,
etc.) without needing a JS-capable reader.

This script only depends on PyMuPDF, so it can be frozen into a single
self-contained .exe with PyInstaller for use on machines with no Python
installed. See build instructions at the bottom of this file.

Usage:
    python mc_pdf_cleaner.py input.pdf [output.pdf]

If run with no arguments (e.g. by double-clicking a frozen .exe), it
will prompt for a file path interactively, which also supports
drag-and-drop of a PDF onto the .exe icon in Windows Explorer.
"""
import sys
import os
import re
import datetime
import traceback

import pymupdf

INFO_KEYS = [
    "headerMessage", "footerMessage", "expirationMessage",
    "expirationHours", "expirationEnabled", "MC_COPIEDON",
    "downloadDate", "MC_USER",
]


def get_info_xref(doc):
    trailer = doc.pdf_trailer()
    m = re.search(r"/Info (\d+) 0 R", trailer)
    return int(m.group(1)) if m else None


def read_info_key(doc, info_xref, key):
    if info_xref is None:
        return None
    kind, val = doc.xref_get_key(info_xref, key)
    return val if kind not in ("null", None) else None


def has_javascript(doc):
    count = 0
    for xref in range(1, doc.xref_length()):
        try:
            obj = doc.xref_object(xref, compressed=False)
        except Exception:
            continue
        if "/JS" in obj or "/JavaScript" in obj:
            count += 1
    return count


def clean_catalog_actions(doc):
    """Remove Catalog-level /OpenAction and /AA (auto-run actions), which
    doc.scrub() empties but does not remove, leaving dangling references."""
    trailer = doc.pdf_trailer()
    m = re.search(r"/Root (\d+) 0 R", trailer)
    if not m:
        return
    root_xref = int(m.group(1))
    for key in ("OpenAction", "AA"):
        kind, _ = doc.xref_get_key(root_xref, key)
        if kind != "null":
            doc.xref_set_key(root_xref, key, "null")


def strip_empty_js_stubs(doc):
    """Null out any leftover <</S /JavaScript /JS ()>> stub objects left by scrub()."""
    changed = False
    for xref in range(1, doc.xref_length()):
        try:
            obj = doc.xref_object(xref, compressed=False)
        except Exception:
            continue
        compact = obj.replace(" ", "").replace("\n", "")
        if "/JS()" in compact and "/S/JavaScript" in compact:
            doc.update_object(xref, "<< >>")
            changed = True
    return changed


def process(input_path, output_path):
    doc = pymupdf.open(input_path)

    info_xref = get_info_xref(doc)
    download_raw = read_info_key(doc, info_xref, "MC_COPIEDON") or read_info_key(doc, info_xref, "downloadDate")
    hours_raw = read_info_key(doc, info_xref, "expirationHours")

    if download_raw and hours_raw:
        try:
            download_ms = int(download_raw)
            hours = float(hours_raw)
            download_dt = datetime.datetime.fromtimestamp(download_ms / 1000, tz=datetime.timezone.utc)
            expiration_dt = download_dt + datetime.timedelta(hours=hours)
            print(f"FYI: MasterControl metadata indicates this copy was downloaded {download_dt} "
                  f"and would have expired {expiration_dt} (informational only -- not displayed or enforced in the output).")
        except Exception:
            pass

    # Note: header/footer text is not baked in -- MC_Header, MC_Footer,
    # and MC_Overlay are all removed entirely so the page contains no
    # MasterControl boilerplate text at all (needed for clean downstream
    # ingestion by other software).
    removed_counts = {"MC_Header": 0, "MC_Footer": 0, "MC_Overlay": 0}
    for page in doc:
        for w in list(page.widgets() or []):
            name = w.field_name
            if name in removed_counts:
                page.delete_widget(w)
                removed_counts[name] += 1

    print(f"Removed {removed_counts['MC_Header']} header field(s), "
          f"{removed_counts['MC_Footer']} footer field(s), "
          f"{removed_counts['MC_Overlay']} overlay field(s)")

    clean_catalog_actions(doc)

    tmp_path = output_path + ".tmp.pdf"
    doc.save(tmp_path, garbage=4, deflate=True, clean=True)
    doc.close()

    doc2 = pymupdf.open(tmp_path)
    try:
        doc2.scrub(javascript=True, metadata=False, embedded_files=False,
                   remove_links=True, reset_fields=False, reset_responses=True, clean_pages=True)
    except RuntimeError:
        # Malformed xref table -- repair with a plain re-save, then retry
        doc2.close()
        repair_doc = pymupdf.open(tmp_path)
        repaired_path = output_path + ".repaired.pdf"
        repair_doc.save(repaired_path, garbage=4, clean=True, deflate=True)
        repair_doc.close()
        os.remove(tmp_path)
        tmp_path = repaired_path
        doc2 = pymupdf.open(tmp_path)
        doc2.scrub(javascript=True, metadata=False, embedded_files=False,
                   remove_links=True, reset_fields=False, reset_responses=True, clean_pages=True)

    doc2.save(output_path, garbage=4, deflate=True, clean=True)
    doc2.close()

    doc3 = pymupdf.open(output_path)
    remaining = has_javascript(doc3)
    if remaining:
        if strip_empty_js_stubs(doc3):
            cleaned_path = output_path + ".clean.pdf"
            doc3.save(cleaned_path, garbage=4, deflate=True, clean=True)
            doc3.close()
            os.replace(cleaned_path, output_path)
            doc3 = pymupdf.open(output_path)
            remaining = has_javascript(doc3)
    doc3.close()

    if os.path.exists(tmp_path):
        os.remove(tmp_path)

    print(f"JavaScript-related objects remaining: {remaining}")
    if remaining == 0:
        print("SUCCESS: no JavaScript remains in the output file.")
    else:
        print("WARNING: some JavaScript-related objects could not be removed automatically.")
    print(f"Output written to: {output_path}")


def main():
    args = sys.argv[1:]
    if len(args) >= 1:
        input_path = args[0]
    else:
        input_path = input("Drag a PDF here (or type its path) and press Enter: ").strip().strip('"')

    if len(args) >= 2:
        output_path = args[1]
    else:
        if input_path.lower().endswith(".pdf"):
            output_path = input_path[:-4] + "-clean.pdf"
        else:
            output_path = input_path + "-clean.pdf"

    try:
        process(input_path, output_path)
    except Exception:
        print("An error occurred:")
        traceback.print_exc()

    try:
        input("\nDone. Press Enter to close this window...")
    except (EOFError, KeyboardInterrupt):
        pass


if __name__ == "__main__":
    main()

# -----------------------------------------------------------------------
# Building a standalone Windows .exe (run these steps ON a Windows 11
# machine -- PyInstaller cannot cross-compile from macOS to Windows):
#
#   1. Install Python 3.11+ from https://python.org (check "Add python.exe
#      to PATH" during setup).
#   2. Open Command Prompt and install dependencies:
#        pip install pymupdf pyinstaller
#   3. cd to the folder containing this script, then run:
#        pyinstaller --onefile --console --name MCPdfCleaner mc_pdf_cleaner.py
#   4. The standalone executable will be at:
#        dist\MCPdfCleaner.exe
#      This single file has no external dependencies and can be copied
#      to any Windows 11 machine (same architecture) without installing
#      Python there.
#
# Usage on the target machine:
#   - Drag and drop a PDF file onto MCPdfCleaner.exe in File Explorer, or
#   - Run from Command Prompt: MCPdfCleaner.exe input.pdf [output.pdf]
# -----------------------------------------------------------------------
