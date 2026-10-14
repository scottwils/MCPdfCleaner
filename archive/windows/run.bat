@echo off
setlocal

where python >nul 2>nul
if errorlevel 1 (
    echo Python was not found on PATH.
    echo Install it from https://python.org - during setup, check the box
    echo "Add python.exe to PATH" - then double-click this file again.
    pause
    exit /b 1
)

python -c "import pymupdf" >nul 2>nul
if errorlevel 1 (
    echo First-time setup: installing the pymupdf library...
    python -m pip install --upgrade pip
    python -m pip install pymupdf
)

if "%~1"=="" (
    python "%~dp0mc_pdf_cleaner.py"
) else (
    python "%~dp0mc_pdf_cleaner.py" %*
)
