@echo off
chcp 65001 >nul
title Desktop Pet
color 0A

echo ========================================
echo     Desktop Pet
echo ========================================
echo.

:: Check if Python is installed
where python >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Python not found!
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

:: Check Python version
python --version
echo.

:: Check if required libraries are installed
echo Checking required libraries...
python -c "import PyQt5, PIL, cv2" 2>nul
if %errorLevel% neq 0 (
    echo [INFO] Installing required libraries...
    echo This may take a few minutes...
    echo.
    
    pip install PyQt5
    pip install Pillow
    pip install opencv-python
    
    echo.
    echo [OK] Libraries installed!
    echo.
)

:: Run the program
echo Starting Desktop Pet...
echo.
echo First run: Select a photo to create your pet
echo.
echo Controls:
echo - Right-click pet: Feed food
echo - Left-click pet: Trigger actions
echo - Drag: Move pet around
echo.
echo Press Ctrl+C to exit
echo ========================================
echo.

python src/main.py

echo.
echo Desktop Pet closed.
pause