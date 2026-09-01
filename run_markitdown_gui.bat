@echo off
REM MarkItDown GUI launcher
REM Place this file in the same folder as markitdown_gui.py

cd /d "%~dp0"

echo Checking for Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python was not found on this computer.
    echo Install Python from https://www.python.org/downloads/ and try again.
    echo During install, check the box that says "Add Python to PATH".
    pause
    exit /b 1
)

echo Checking for the markitdown package...
python -c "import markitdown" >nul 2>&1
if errorlevel 1 (
    echo The markitdown package was not found through pip.
    echo Trying to install it from your local copy...

    if exist "C:\Users\ozd504\markitdown\packages\markitdown\pyproject.toml" (
        python -m pip install -e "C:\Users\ozd504\markitdown\packages\markitdown[pdf,docx,pptx,xlsx,xls,outlook]"
    ) else if exist "C:\Users\ozd504\markitdown\pyproject.toml" (
        python -m pip install -e "C:\Users\ozd504\markitdown[pdf,docx,pptx,xlsx,xls,outlook]"
    ) else (
        echo Could not find a pyproject.toml file in C:\Users\ozd504\markitdown.
        echo Open that folder and look for a pyproject.toml file, then tell me
        echo which subfolder it is in so I can point the installer at it.
        pause
        exit /b 1
    )

    python -c "import markitdown" >nul 2>&1
    if errorlevel 1 (
        echo The install did not finish correctly. See the messages above for the reason.
        pause
        exit /b 1
    )
)

echo Starting MarkItDown GUI...
python markitdown_gui.py

pause
