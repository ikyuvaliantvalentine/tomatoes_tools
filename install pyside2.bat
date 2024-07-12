@echo off
REM Change directory to the Blender directory (assuming the script is placed inside the Blender directory)
cd /d "%~dp0"

REM Set the paths for Blender's Python executable and scripts
set PYTHON_DIR=%~dp03.6\python\bin
set SCRIPT_DIR=%~dp03.6\python\Scripts

REM Check if pip is already installed
%PYTHON_DIR%\python.exe -m ensurepip
%PYTHON_DIR%\python.exe -m pip --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Pip is already installed.
) else (
    REM Download get-pip.py using curl
    if exist get-pip.py (
        echo get-pip.py already exists.
    ) else (
        curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    )

    REM Install pip
    %PYTHON_DIR%\python.exe get-pip.py
)

REM Check if PySide2 is already installed
%SCRIPT_DIR%\pip.exe show PySide2 >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo PySide2 is already installed.
) else (
    REM Install PySide2 using pip
    %SCRIPT_DIR%\pip.exe install PySide2 --no-warn-script-location
    echo PySide2 installation complete.
)

pause
