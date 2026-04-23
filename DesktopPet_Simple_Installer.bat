@echo off
chcp 65001 >nul
title Desktop Pet Installer
color 0A

echo ========================================
echo     Desktop Pet - Simple Installer
echo ========================================
echo.
echo This script will install Desktop Pet for you
echo It will automatically install Python and all required libraries
echo.
echo Press any key to start...
pause >nul

:: Set variables
set INSTALL_DIR=%USERPROFILE%\Desktop\DesktopPet
set TEMP_DIR=%TEMP%\desktop_pet_temp
set PYTHON_URL=https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe

:: Create temp directory
if not exist "%TEMP_DIR%" mkdir "%TEMP_DIR%"

echo.
echo ========================================
echo Step 1: Check Python
echo ========================================
echo.

:: Check if Python is installed
where python >nul 2>&1
if %errorLevel% equ 0 (
    python --version
    echo [OK] Python is installed
    goto :check_pip
)

echo [INFO] Python not found
echo [INFO] Downloading Python installer...

:: Download Python installer
echo Downloading Python...
powershell -Command "Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%TEMP_DIR%\python_installer.exe'"

if not exist "%TEMP_DIR%\python_installer.exe" (
    echo [ERROR] Failed to download Python
    echo Please download Python manually from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python installer downloaded
echo.
echo [INFO] Starting Python installation...
echo IMPORTANT: Check "Add Python to PATH" during installation!
echo.
echo Press any key to start Python installer...
pause >nul

start /wait "%TEMP_DIR%\python_installer.exe"

:: Wait for installation
timeout /t 3 /nobreak >nul

:check_pip
echo.
echo Checking pip...
where pip >nul 2>&1
if %errorLevel% equ 0 (
    pip --version
    echo [OK] pip is installed
    goto :download_files
)

echo [INFO] Installing pip...
python -m ensurepip --upgrade
echo [OK] pip installed

:download_files
echo.
echo ========================================
echo Step 2: Download Desktop Pet
echo ========================================
echo.

echo [INFO] Creating installation directory: %INSTALL_DIR%
if exist "%INSTALL_DIR%" (
    echo [INFO] Backup existing installation...
    if exist "%INSTALL_DIR%_backup" rmdir /s /q "%INSTALL_DIR%_backup"
    move "%INSTALL_DIR%" "%INSTALL_DIR%_backup"
)

mkdir "%INSTALL_DIR%" 2>nul
mkdir "%INSTALL_DIR%\src" 2>nul
mkdir "%INSTALL_DIR%\assets" 2>nul
mkdir "%INSTALL_DIR%\assets\images" 2>nul
mkdir "%INSTALL_DIR%\config" 2>nul

echo [INFO] Downloading program files...

:: Download main files
echo Downloading main program...
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/luomodeshang/desktop-pet/main/src/main.py' -OutFile '%INSTALL_DIR%\src\main.py'"

echo Downloading config file...
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/luomodeshang/desktop-pet/main/config/config.json' -OutFile '%INSTALL_DIR%\config\config.json'"

echo Downloading run script...
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/luomodeshang/desktop-pet/main/run.bat' -OutFile '%INSTALL_DIR%\run.bat'"

echo Downloading default avatar...
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/luomodeshang/desktop-pet/main/assets/images/default_avatar.png' -OutFile '%INSTALL_DIR%\assets\images\default_avatar.png'"

echo Downloading icon...
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/luomodeshang/desktop-pet/main/assets/images/icon.ico' -OutFile '%INSTALL_DIR%\assets\images\icon.ico'"

echo Downloading user guide...
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/luomodeshang/desktop-pet/main/USER_GUIDE_%E5%B0%8F%E7%99%BD%E7%89%88.md' -OutFile '%INSTALL_DIR%\USER_GUIDE.md'"

echo [OK] Files downloaded!

echo.
echo ========================================
echo Step 3: Install Python Libraries
echo ========================================
echo.

echo [INFO] Installing required Python libraries...
echo This may take a few minutes...

cd /d "%INSTALL_DIR%"

echo Installing PyQt5...
pip install PyQt5

echo Installing Pillow...
pip install Pillow

echo Installing opencv-python...
pip install opencv-python

echo [OK] Libraries installed!

echo.
echo ========================================
echo Step 4: Create Shortcuts
echo ========================================
echo.

echo [INFO] Creating desktop shortcut...

:: Create desktop shortcut
echo Set WshShell = CreateObject("WScript.Shell") > "%TEMP_DIR%\shortcut.vbs"
echo Set oShellLink = WshShell.CreateShortcut("%USERPROFILE%\Desktop\DesktopPet.lnk") >> "%TEMP_DIR%\shortcut.vbs"
echo oShellLink.TargetPath = "%INSTALL_DIR%\run.bat" >> "%TEMP_DIR%\shortcut.vbs"
echo oShellLink.WorkingDirectory = "%INSTALL_DIR%" >> "%TEMP_DIR%\shortcut.vbs"
echo oShellLink.IconLocation = "%INSTALL_DIR%\assets\images\icon.ico" >> "%TEMP_DIR%\shortcut.vbs"
echo oShellLink.Save >> "%TEMP_DIR%\shortcut.vbs"

cscript //nologo "%TEMP_DIR%\shortcut.vbs"

if exist "%USERPROFILE%\Desktop\DesktopPet.lnk" (
    echo [OK] Desktop shortcut created!
) else (
    echo [WARNING] Failed to create desktop shortcut
)

echo.
echo ========================================
echo Step 5: Installation Complete!
echo ========================================
echo.

echo [SUCCESS] Desktop Pet installed successfully!
echo.
echo Installation location: %INSTALL_DIR%
echo.
echo To start the program:
echo 1. Double-click "DesktopPet" on your desktop
echo 2. Or run: %INSTALL_DIR%\run.bat
echo.
echo First run: Select a photo to create your pet
echo.
echo Basic controls:
echo - Right-click pet: Feed food
echo - Left-click pet: Trigger actions
echo - Drag: Move pet around
echo.
echo ========================================
echo Press 1 to start program, 2 to open folder, any other key to exit
choice /c 12 /n /m "Choose:"

if errorlevel 2 (
    echo Opening installation folder...
    explorer "%INSTALL_DIR%"
) else if errorlevel 1 (
    echo Starting Desktop Pet...
    start "" "%INSTALL_DIR%\run.bat"
)

:: Clean up temp files
if exist "%TEMP_DIR%" rmdir /s /q "%TEMP_DIR%"

echo.
echo Thank you for installing Desktop Pet!
pause
exit /b 0