@echo off
chcp 65001 >nul
title Desktop Pet

echo ========================================
echo     Desktop Pet v4.0.1
echo ========================================
echo.

python --version >nul 2>&1
if errorlevel 1 goto nopython

echo Python found:
python --version
echo.

cd /d "%~dp0"
echo Checking required libraries...

python -c "import PyQt5" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing PyQt5...
    pip install PyQt5
)

python -c "import PIL" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing Pillow...
    pip install Pillow
)

:: Check & fix OpenCV (MediaPipe needs compatible version)
python -c "import cv2; import mediapipe" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Fixing OpenCV/MediaPipe compatibility...
    pip uninstall opencv-contrib-python opencv-python opencv-python-headless -y >nul 2>&1
    pip install --user opencv-python==4.9.0.80
)

:: Install MediaPipe if missing
python -c "import mediapipe" >nul 2>&1
if errorlevel 1 goto install_mp

echo.
echo [OK] All libraries ready!
echo.

:run_pet
python src\main.py
if errorlevel 1 (
    echo.
    echo [ERROR] Program exited with error code %errorLevel%
    pause
)
goto end

:install_mp
if exist "deps\mediapipe-0.10.21-cp39-cp39-win_amd64.whl" goto install_local
echo [INFO] Installing MediaPipe from PyPI...
pip install --user mediapipe
echo.
goto run_pet

:install_local
echo [INFO] Installing MediaPipe from local package...
pip install --user "deps\mediapipe-0.10.21-cp39-cp39-win_amd64.whl"
echo.
goto run_pet

:nopython
echo [ERROR] Python not found!
echo Please install Python 3.10+ from https://www.python.org/downloads/
echo.
pause

:end
