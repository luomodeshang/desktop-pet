@echo off
chcp 65001 >nul
title Desktop Pet Quick Fix
color 0A

echo ========================================
echo     Desktop Pet - Quick Fix
echo ========================================
echo.
echo This script fixes missing source files
echo in your existing installation.
echo.
echo Press any key to continue...
pause >nul

:: Set installation directory
set INSTALL_DIR=%~dp0
if "%INSTALL_DIR%"=="" set INSTALL_DIR=%CD%\

echo.
echo Installation directory: %INSTALL_DIR%
echo.

:: Check if we're in the right directory
if not exist "%INSTALL_DIR%\run.bat" (
    echo [ERROR] Not in Desktop Pet installation directory!
    echo.
    echo Please run this script from your DesktopPet folder.
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Step 1: Check existing files
echo ========================================
echo.

echo Checking src directory...
if exist "%INSTALL_DIR%\src\main.py" (
    echo [OK] main.py exists
) else (
    echo [WARNING] main.py not found
    set NEED_SRC=1
)

echo Checking assets...
if exist "%INSTALL_DIR%\assets\images\default_avatar.png" (
    echo [OK] Assets exist
) else (
    echo [WARNING] Assets not found
    set NEED_ASSETS=1
)

echo.
echo ========================================
echo Step 2: Download missing files
echo ========================================
echo.

set GITHUB_BASE=https://raw.githubusercontent.com/luomodeshang/desktop-pet/main

if "%NEED_SRC%"=="1" (
    echo [INFO] Creating src directory...
    mkdir "%INSTALL_DIR%\src" 2>nul
    
    echo Downloading main.py...
    powershell -Command "Invoke-WebRequest -Uri '%GITHUB_BASE%/src/main.py' -OutFile '%INSTALL_DIR%\src\main.py'" 2>nul
    
    echo Downloading pet.py...
    powershell -Command "Invoke-WebRequest -Uri '%GITHUB_BASE%/src/pet.py' -OutFile '%INSTALL_DIR%\src\pet.py'" 2>nul
    
    echo Downloading ui.py...
    powershell -Command "Invoke-WebRequest -Uri '%GITHUB_BASE%/src/ui.py' -OutFile '%INSTALL_DIR%\src\ui.py'" 2>nul
    
    echo Downloading utils.py...
    powershell -Command "Invoke-WebRequest -Uri '%GITHUB_BASE%/src/utils.py' -OutFile '%INSTALL_DIR%\src\utils.py'" 2>nul
    
    echo [OK] Source files downloaded!
)

if "%NEED_ASSETS%"=="1" (
    echo [INFO] Creating assets directories...
    mkdir "%INSTALL_DIR%\assets" 2>nul
    mkdir "%INSTALL_DIR%\assets\images" 2>nul
    
    echo Downloading default_avatar.png...
    powershell -Command "Invoke-WebRequest -Uri '%GITHUB_BASE%/assets/images/default_avatar.png' -OutFile '%INSTALL_DIR%\assets\images\default_avatar.png'" 2>nul
    
    echo Downloading icon.ico...
    powershell -Command "Invoke-WebRequest -Uri '%GITHUB_BASE%/assets/images/icon.ico' -OutFile '%INSTALL_DIR%\assets\images\icon.ico'" 2>nul
    
    echo [OK] Assets downloaded!
)

echo.
echo ========================================
echo Step 3: Create simple run script
echo ========================================
echo.

echo [INFO] Creating simple_run.bat...

echo @echo off > "%INSTALL_DIR%\simple_run.bat"
echo chcp 65001 ^>nul >> "%INSTALL_DIR%\simple_run.bat"
echo title Desktop Pet >> "%INSTALL_DIR%\simple_run.bat"
echo. >> "%INSTALL_DIR%\simple_run.bat"
echo echo Starting Desktop Pet... >> "%INSTALL_DIR%\simple_run.bat"
echo echo. >> "%INSTALL_DIR%\simple_run.bat"
echo. >> "%INSTALL_DIR%\simple_run.bat"
echo :: Check Python >> "%INSTALL_DIR%\simple_run.bat"
echo python --version 2^>nul >> "%INSTALL_DIR%\simple_run.bat"
echo if errorlevel 1 ( >> "%INSTALL_DIR%\simple_run.bat"
echo     echo ERROR: Python not installed or not in PATH >> "%INSTALL_DIR%\simple_run.bat"
echo     echo. >> "%INSTALL_DIR%\simple_run.bat"
echo     echo Download Python from: https://www.python.org/downloads/ >> "%INSTALL_DIR%\simple_run.bat"
echo     echo Install Python 3.10+ and check "Add Python to PATH" >> "%INSTALL_DIR%\simple_run.bat"
echo     pause >> "%INSTALL_DIR%\simple_run.bat"
echo     exit /b 1 >> "%INSTALL_DIR%\simple_run.bat"
echo ) >> "%INSTALL_DIR%\simple_run.bat"
echo. >> "%INSTALL_DIR%\simple_run.bat"
echo :: Run the program >> "%INSTALL_DIR%\simple_run.bat"
echo cd /d "%%~dp0" >> "%INSTALL_DIR%\simple_run.bat"
echo python src\main.py >> "%INSTALL_DIR%\simple_run.bat"
echo. >> "%INSTALL_DIR%\simple_run.bat"
echo pause >> "%INSTALL_DIR%\simple_run.bat"

echo [OK] Simple run script created!

echo.
echo ========================================
echo Step 4: Fix complete!
echo ========================================
echo.

echo [SUCCESS] Desktop Pet fixed!
echo.
echo Files in your installation:
dir "%INSTALL_DIR%\src" 2>nul || echo src directory not found
echo.
echo To run the program:
echo 1. Double-click simple_run.bat in this folder
echo 2. Or run: "%INSTALL_DIR%\simple_run.bat"
echo.
echo If Python is not installed:
echo 1. Download from https://www.python.org/downloads/
echo 2. Install Python 3.10+
echo 3. CHECK "Add Python to PATH" during installation
echo.
echo ========================================
echo Press 1 to run program now, 2 to open folder, any other key to exit
echo.

choice /c 12 /n /m "Choose:"

if errorlevel 2 (
    echo Opening installation folder...
    explorer "%INSTALL_DIR%"
) else if errorlevel 1 (
    echo Starting Desktop Pet...
    start "" "%INSTALL_DIR%\simple_run.bat"
)

echo.
echo Fix complete! If you still have issues:
echo 1. Make sure Python is installed
echo 2. Run simple_run.bat
echo 3. It will show any errors
pause
exit /b 0