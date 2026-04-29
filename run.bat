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

:: Fix OpenCV
python -c "import cv2" >nul 2>&1
if errorlevel 1 goto opencv_fix

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

:opencv_fix
echo [INFO] Setting up OpenCV...
pip uninstall opencv-contrib-python opencv-python -y >nul 2>&1
pip install --user opencv-python==4.9.0.80
echo.
python -c "import mediapipe" >nul 2>&1
if errorlevel 1 goto install_mp
goto run_pet

:install_mp
:: Detect Python version and pick the right whl
python -c "import sys; v=sys.version_info; print(f'cp{v.major}{v.minor}')" > "%temp%\pyver.txt"
set /p PYVER=<"%temp%\pyver.txt"

if exist "deps\mediapipe-0.10.21-%PYVER%-win_amd64.whl" (
    echo [INFO] Installing MediaPipe for Python %PYVER%...
    pip install --user "deps\mediapipe-0.10.21-%PYVER%-win_amd64.whl"
) else (
    echo [INFO] No local MediaPipe for Python %PYVER%, trying PyPI...
    pip install --user mediapipe
)
echo.
goto run_pet

:nopython
echo [ERROR] Python not found!
echo Please install Python 3.10+ from https://www.python.org/downloads/
echo.
pause

:end
