@echo off
chcp 65001 >nul
title Desktop Pet

echo ========================================
echo     Desktop Pet
echo ========================================
echo.

:: Check Python
python --version 2>nul
if errorlevel 1 (
    echo [ERROR] Python not found or not in PATH!
    echo.
    echo Please install Python 3.10+ from:
    echo https://www.python.org/downloads/
    echo.
    echo IMPORTANT: During installation, CHECK "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo Python found:
python --version
echo.

:: Make sure we're in the right directory
cd /d "%~dp0"

:: Check if required libraries are installed
echo Checking required libraries...
python -c "import PyQt5" 2>nul
if %errorLevel% neq 0 (
    echo [INFO] Installing PyQt5...
    echo This may take a minute...
    pip install PyQt5
    echo.
)

python -c "import PIL" 2>nul
if %errorLevel% neq 0 (
    echo [INFO] Installing Pillow...
    pip install Pillow
    echo.
)

python -c "import cv2" 2>nul
if %errorLevel% neq 0 (
    echo [INFO] Installing opencv-python...
    pip install opencv-python
    echo.
)

echo [OK] All libraries ready!
echo.
echo ========================================
echo Starting Desktop Pet...
echo.
echo Controls:
echo - Left-click: Trigger action
echo - Right-click: Feed food
echo - Drag: Move pet
echo - Tray menu: More options
echo ========================================
echo.

:: Run the program
python src\main.py

if %errorLevel% neq 0 (
    echo.
    echo [ERROR] Program exited with error code %errorLevel%
    echo.
    pause
)