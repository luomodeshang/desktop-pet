@echo off
chcp 65001 >nul
title Desktop Pet Icon Manager
color 0A

echo ========================================
echo     Desktop Pet - Icon Manager
echo ========================================
echo.
echo This tool helps you customize the desktop shortcut icon
echo.
echo Press any key to continue...
pause >nul

:: Set variables
set INSTALL_DIR=%~dp0
if "%INSTALL_DIR%"=="" set INSTALL_DIR=%CD%\

echo.
echo Installation directory: %INSTALL_DIR%
echo.

:: Check Python
python --version 2>nul
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Step 1: Install required libraries
echo ========================================
echo.

echo [INFO] Checking required libraries...

python -c "import PyQt5, win32com" 2>nul
if %errorLevel% neq 0 (
    echo [INFO] Installing PyQt5 and pywin32...
    pip install PyQt5
    pip install pywin32
    echo.
    echo [OK] Libraries installed!
) else (
    echo [OK] All required libraries are already installed.
)

echo.
echo ========================================
echo Step 2: Create icon directories
echo ========================================
echo.

echo [INFO] Creating icon directories...

mkdir "%INSTALL_DIR%\assets\icons" 2>nul
mkdir "%INSTALL_DIR%\user_icons" 2>nul

echo [OK] Directories created!

echo.
echo ========================================
echo Step 3: Copy default icons
echo ========================================
echo.

echo [INFO] Copying default icons...

:: Copy default icon
if exist "%INSTALL_DIR%\assets\images\icon.ico" (
    copy "%INSTALL_DIR%\assets\images\icon.ico" "%INSTALL_DIR%\assets\icons\default.ico" >nul
    echo [OK] Default icon copied.
) else (
    echo [WARNING] Default icon not found.
)

echo.
echo ========================================
echo Step 4: Start Icon Manager
echo ========================================
echo.

echo [INFO] Starting Icon Manager GUI...
echo.
echo Instructions:
echo 1. Click "Add Icon" to add your own icon files
echo 2. Double-click an icon to select it
echo 3. The desktop shortcut will be updated automatically
echo.
echo Supported formats: .ico, .png, .jpg, .bmp
echo Recommended size: 256x256 or 128x128
echo.
echo Press any key to start...
pause >nul

:: Run the icon manager
cd /d "%INSTALL_DIR%"
python src\icon_manager_gui.py

echo.
echo ========================================
echo Icon Manager closed
echo ========================================
echo.
echo Your desktop shortcut icon has been updated!
echo.
echo To change icon again:
echo 1. Run this script: icon_manager.bat
echo 2. Or run: python src\icon_manager_gui.py
echo.
echo Press any key to exit...
pause
exit /b 0