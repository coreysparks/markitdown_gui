@echo off
REM MarkItDown GUI launcher
REM Place this file in the same folder as markitdown_gui.py

cd /d "%~dp0"

echo Checking for Python...
set "PYTHON_EXE=python"
where python >nul 2>&1
if errorlevel 1 set "PYTHON_EXE="
if not defined PYTHON_EXE (
    if exist "%LOCALAPPDATA%\miniforge3\python.exe" set "PYTHON_EXE=%LOCALAPPDATA%\miniforge3\python.exe"
)
if not defined PYTHON_EXE (
    echo Python was not found on this computer.
    echo Install Python from https://www.python.org/downloads/ and try again.
    echo During install, check the box that says "Add Python to PATH".
    pause
    exit /b 1
)

"%PYTHON_EXE%" --version >nul 2>&1
if errorlevel 1 (
    if exist "%LOCALAPPDATA%\miniforge3\python.exe" (
        set "PYTHON_EXE=%LOCALAPPDATA%\miniforge3\python.exe"
    ) else (
        echo Python was not found on this computer.
        echo Install Python from https://www.python.org/downloads/ and try again.
        echo During install, check the box that says "Add Python to PATH".
        pause
        exit /b 1
    )
)

echo Using Python at: %PYTHON_EXE%

echo Checking for the markitdown package...
"%PYTHON_EXE%" -c "import markitdown" >nul 2>&1
if errorlevel 1 (
    echo The markitdown package was not found. Installing it from PyPI...
    "%PYTHON_EXE%" -m pip install "markitdown[all]"

    "%PYTHON_EXE%" -c "import markitdown" >nul 2>&1
    if errorlevel 1 (
        echo The install did not finish correctly. See the messages above for the reason.
        pause
        exit /b 1
    )
)

echo Starting MarkItDown GUI...
"%PYTHON_EXE%" markitdown_gui.py

pause
