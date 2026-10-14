#!/bin/bash
cd "$(dirname "$0")"

if ! command -v python3 >/dev/null 2>&1; then
    echo "python3 was not found."
    echo "Install the Xcode Command Line Tools by running:"
    echo "    xcode-select --install"
    echo "then run this script again."
    read -p "Press Enter to close..."
    exit 1
fi

if ! python3 -c "import pymupdf" >/dev/null 2>&1; then
    echo "First-time setup: installing the pymupdf library..."
    python3 -m pip install --upgrade pip
    python3 -m pip install pymupdf
fi

python3 "$(dirname "$0")/mc_pdf_cleaner.py" "$@"

read -p "Press Enter to close this window..."
