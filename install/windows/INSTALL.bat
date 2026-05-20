@echo off
setlocal EnableDelayedExpansion
title Registral Space Analysis - Install (Windows)
cd /d "%~dp0\..\.."

echo.
echo ============================================================
echo   Registral Space Analysis - One-click installer (Windows)
echo ============================================================
echo.
echo This will install the symbolic-score registral dispersion
echo tool and create a shortcut launcher in this folder.
echo.
echo Copyright (c) 2026 Luis Raimundo. All rights reserved.
echo.

set "PY="
set "PYARG="

where py >nul 2>&1
if %ERRORLEVEL%==0 (
    for %%V in (3.12 3.11 3.10) do (
        py -%%V -c "import sys; assert sys.version_info>=(3,10)" >nul 2>&1
        if !ERRORLEVEL!==0 (
            set "PY=py"
            set "PYARG=-%%V"
            goto :found_py
        )
    )
)

where python >nul 2>&1
if %ERRORLEVEL%==0 (
    python -c "import sys; assert sys.version_info>=(3,10)" >nul 2>&1
    if !ERRORLEVEL!==0 (
        set "PY=python"
        set "PYARG="
        goto :found_py
    )
)

echo Python 3.10 or newer was not found on this computer.
echo.
echo Trying to install Python via winget (may ask for approval)...
where winget >nul 2>&1
if %ERRORLEVEL%==0 (
    winget install --id Python.Python.3.12 -e --accept-source-agreements --accept-package-agreements
    set "PY=py"
    set "PYARG=-3.12"
    goto :found_py
)

echo.
echo Could not install Python automatically.
echo Please install Python 3.10+ from https://www.python.org/downloads/
echo IMPORTANT: check "Add python.exe to PATH" during installation.
echo Then run this installer again.
echo.
pause
exit /b 1

:found_py
echo Using: %PY% %PYARG%
echo.

if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment...
    %PY% %PYARG% -m venv .venv
    if errorlevel 1 (
        echo Failed to create virtual environment.
        pause
        exit /b 1
    )
)

echo Upgrading pip and installing Registral Space Analysis...
call ".venv\Scripts\activate.bat"
python -m pip install --upgrade pip
python -m pip install -e .
if errorlevel 1 (
    echo Installation failed. See messages above.
    pause
    exit /b 1
)

echo.
echo Creating launcher scripts...
(
echo @echo off
echo cd /d "%%~dp0"
echo call ".venv\Scripts\activate.bat"
echo python -m registral_dispersion
echo if errorlevel 1 pause
) > "Launch-Registral-Space-Analysis.bat"

(
echo @echo off
echo cd /d "%%~dp0"
echo call ".venv\Scripts\activate.bat"
echo python -m registral_dispersion summarize %%*
) > "Summarize-Score.bat"

echo.
echo ============================================================
echo   Installation complete.
echo ============================================================
echo.
echo To open the analysis interface, double-click:
echo   Launch-Registral-Space-Analysis.bat
echo.
echo For a one-number global summary from the command line:
echo   Summarize-Score.bat --score "path\to\score.musicxml"
echo.
set /p RUN="Launch the interface now? [Y/n]: "
if /i "!RUN!"=="n" goto :done
call "Launch-Registral-Space-Analysis.bat"
:done
pause
exit /b 0
