@echo off
REM Apion - Installation Script for Windows

echo.
echo ================================
echo Apion - HTTP Client Pro
echo ================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.7+ from https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python detected
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate venv
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ================================
echo Installation complete!
echo ================================
echo.
echo To run Apion:
echo   apion.bat
echo.
echo Or manually:
echo   venv\Scripts\activate
echo   python http_client_stable.py
echo.

REM Create launcher batch file
(
echo @echo off
echo call "%%~dp0venv\Scripts\activate.bat"
echo python "%%~dp0http_client_stable.py" %%*
) > apion.bat

echo Quick start: apion.bat
echo.
pause
