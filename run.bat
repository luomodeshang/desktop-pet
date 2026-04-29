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
    echo [INFO] Installing opencv-python (v4.9.0 for Python 3.9 compat)...
    pip install opencv-python==4.9.0.80 -i https://pypi.tuna.tsinghua.edu.cn/simple || pip install opencv-python==4.9.0.80 -i https://mirrors.aliyun.com/pypi/simple
    echo.
)

:: Install mediapipe from local whl if available (avoid network issues in China)
python -c "import mediapipe" 2>nul
if %errorLevel% neq 0 (
    if exist deps\mediapipe-0.10.21-cp39-cp39-win_amd64.whl (
        echo [INFO] Installing MediaPipe from local package...
        pip install deps\mediapipe-0.10.21-cp39-cp39-win_amd64.whl -i https://pypi.tuna.tsinghua.edu.cn/simple || pip install deps\mediapipe-0.10.21-cp39-cp39-win_amd64.whl -i https://mirrors.aliyun.com/pypi/simple
        echo.
    ) else (
        echo [INFO] MediaPipe not found, trying pip install...
        pip install mediapipe -i https://pypi.tuna.tsinghua.edu.cn/simple || pip install mediapipe -i https://mirrors.aliyun.com/pypi/simple
        echo.
    )
)

echo [OK] All libraries ready!
echo.

:: Run the program
python src\main.py

if %errorLevel% neq 0 (
    echo.
    echo [ERROR] Program exited with error code %errorLevel%
    echo.
    pause
)