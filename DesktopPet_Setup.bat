:: Desktop Pet - One-click setup script
:: This script downloads and installs everything you need.

@echo off
chcp 65001 >nul
title Desktop Pet Setup

setlocal enabledelayedexpansion

set "DL_URL=https://github.com/luomodeshang/desktop-pet/archive/refs/heads/main.zip"
set "TEMP_ZIP=%TEMP%\desktop-pet.zip"
set "EXTRACT_DIR=%TEMP%\desktop-pet-extract"

echo =============================================
echo        Desktop Pet - Setup
echo =============================================
echo.

:: --- Step 1: Check Python ---
echo [1/4] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found!
    echo Please install Python 3.10+ from:
    echo   https://www.python.org/downloads/
    echo.
    echo During install, check "Add Python to PATH"
    pause
    exit /b 1
)
for /f "tokens=2 delims= " %%a in ('python --version 2^>^&1') do set "PY_VER=%%a"
echo   Found: Python %PY_VER%
echo.

:: --- Step 2: Download ---
echo [2/4] Downloading Desktop Pet...

:: Create target folder on Desktop
set "TARGET=%USERPROFILE%\Desktop\DesktopPet"
if not exist "%TARGET%" mkdir "%TARGET%"

:: Try curl (Windows 10+)
where curl >nul 2>&1
if errorlevel 1 (
    echo Downloading with PowerShell...
    powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri '%DL_URL%' -OutFile '%TEMP_ZIP%' -UseBasicParsing}"
) else (
    curl -L -o "%TEMP_ZIP%" "%DL_URL%"
)

if not exist "%TEMP_ZIP%" (
    echo Failed to download! Check internet connection.
    pause
    exit /b 1
)
echo   Downloaded successfully
echo.

:: --- Step 3: Extract ---
echo [3/4] Installing files...

:: Clean previous extract
if exist "%EXTRACT_DIR%" rmdir /s /q "%EXTRACT_DIR%"
mkdir "%EXTRACT_DIR%"

:: Extract ZIP using PowerShell
powershell -Command "& {Expand-Archive -Path '%TEMP_ZIP%' -DestinationPath '%EXTRACT_DIR%' -Force}"
xcopy "%EXTRACT_DIR%\desktop-pet-main\*" "%TARGET%" /E /I /Y >nul

:: Cleanup
del "%TEMP_ZIP%" 2>nul
rmdir /s /q "%EXTRACT_DIR%" 2>nul
echo   Installed to: %TARGET%
echo.

:: --- Step 4: Install Dependencies ---
echo [4/4] Installing Python libraries (first time may take a while)...
echo   Installing PyQt5...
pip install PyQt5 -q
echo   Installing Pillow...
pip install Pillow -q
echo   Installing opencv-python...
pip install opencv-python -q
echo.

:: --- Done ---
echo =============================================
echo  Installation complete!
echo =============================================
echo.
echo  Files location: %TARGET%
echo.
echo  To start the pet:
echo   1. Open DesktopPet folder
echo   2. Double-click run.bat
echo.
echo  Or go to: %TARGET%
echo  and run:  run.bat
echo.
echo  Press any key to open the folder...
pause >nul
start "" "%TARGET%"
echo.
echo  Done! Have fun with your Desktop Pet ^_^
pause
