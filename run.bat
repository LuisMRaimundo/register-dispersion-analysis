@echo off
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" (
    call ".venv\Scripts\activate.bat"
    python -m registral_dispersion
) else (
    echo Virtual environment not found. Please run install\windows\INSTALL.bat first.
    pause
)
