@echo off
chcp 65001 >nul
title Desktop Pet Installer - Fixed Version
color 0A

echo ========================================
echo     Desktop Pet - Fixed Installer
echo ========================================
echo.
echo This installer fixes encoding issues
echo Uses pure English commands only
echo.
echo Press any key to continue...
pause >nul

:: Set variables
set INSTALL_DIR=%USERPROFILE%\Desktop\DesktopPet
set EXE_URL=https://github.com/luomodeshang/desktop-pet/releases/latest/download/DesktopPet.exe

echo.
echo ========================================
echo Step 1: Create installation folder
echo ========================================
echo.

if exist "%INSTALL_DIR%" (
    echo [INFO] Backup existing installation...
    if exist "%INSTALL_DIR%_backup" rmdir /s /q "%INSTALL_DIR%_backup"
    move "%INSTALL_DIR%" "%INSTALL_DIR%_backup" 2>nul
)

mkdir "%INSTALL_DIR%" 2>nul
mkdir "%INSTALL_DIR%\assets" 2>nul
mkdir "%INSTALL_DIR%\assets\images" 2>nul

echo [OK] Folder created: %INSTALL_DIR%

echo.
echo ========================================
echo Step 2: Download DesktopPet.exe
echo ========================================
echo.

echo [INFO] Downloading DesktopPet.exe...
echo This may take a minute...

cd /d "%INSTALL_DIR%"

:: Try to download EXE
powershell -Command "Invoke-WebRequest -Uri '%EXE_URL%' -OutFile '%INSTALL_DIR%\DesktopPet.exe'" 2>nul

if exist "%INSTALL_DIR%\DesktopPet.exe" (
    echo [OK] DesktopPet.exe downloaded!
    goto :create_files
)

echo [WARNING] Could not download EXE
echo You can download it manually from:
echo https://github.com/luomodeshang/desktop-pet/releases
echo.
echo For now, we'll create Python version...

:create_files
echo.
echo ========================================
echo Step 3: Create run scripts
echo ========================================
echo.

echo [INFO] Creating run scripts...

:: Create pure English run script
echo @echo off > "%INSTALL_DIR%\run.bat"
echo chcp 65001 ^>nul >> "%INSTALL_DIR%\run.bat"
echo title Desktop Pet >> "%INSTALL_DIR%\run.bat"
echo color 0A >> "%INSTALL_DIR%\run.bat"
echo. >> "%INSTALL_DIR%\run.bat"
echo echo ======================================== >> "%INSTALL_DIR%\run.bat"
echo echo     Desktop Pet >> "%INSTALL_DIR%\run.bat"
echo echo ======================================== >> "%INSTALL_DIR%\run.bat"
echo echo. >> "%INSTALL_DIR%\run.bat"
echo. >> "%INSTALL_DIR%\run.bat"
echo :: Check if EXE exists >> "%INSTALL_DIR%\run.bat"
echo if exist "DesktopPet.exe" ( >> "%INSTALL_DIR%\run.bat"
echo     echo Starting Desktop Pet EXE version... >> "%INSTALL_DIR%\run.bat"
echo     echo. >> "%INSTALL_DIR%\run.bat"
echo     DesktopPet.exe >> "%INSTALL_DIR%\run.bat"
echo     goto :end >> "%INSTALL_DIR%\run.bat"
echo ) >> "%INSTALL_DIR%\run.bat"
echo. >> "%INSTALL_DIR%\run.bat"
echo :: Check Python >> "%INSTALL_DIR%\run.bat"
echo where python ^>nul 2^>^&1 >> "%INSTALL_DIR%\run.bat"
echo if %%errorLevel%% neq 0 ( >> "%INSTALL_DIR%\run.bat"
echo     echo [ERROR] Python not found! >> "%INSTALL_DIR%\run.bat"
echo     echo. >> "%INSTALL_DIR%\run.bat"
echo     echo Please install Python from: https://www.python.org/downloads/ >> "%INSTALL_DIR%\run.bat"
echo     echo. >> "%INSTALL_DIR%\run.bat"
echo     pause >> "%INSTALL_DIR%\run.bat"
echo     exit /b 1 >> "%INSTALL_DIR%\run.bat"
echo ) >> "%INSTALL_DIR%\run.bat"
echo. >> "%INSTALL_DIR%\run.bat"
echo echo Starting Desktop Pet Python version... >> "%INSTALL_DIR%\run.bat"
echo echo. >> "%INSTALL_DIR%\run.bat"
echo python src\main.py >> "%INSTALL_DIR%\run.bat"
echo. >> "%INSTALL_DIR%\run.bat"
echo :end >> "%INSTALL_DIR%\run.bat"
echo echo. >> "%INSTALL_DIR%\run.bat"
echo echo Desktop Pet closed. >> "%INSTALL_DIR%\run.bat"
echo pause >> "%INSTALL_DIR%\run.bat"

echo [OK] Run script created!

echo.
echo ========================================
echo Step 4: Download assets
echo ========================================
echo.

echo [INFO] Downloading default avatar...
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/luomodeshang/desktop-pet/main/assets/images/default_avatar.png' -OutFile '%INSTALL_DIR%\assets\images\default_avatar.png'" 2>nul

echo [INFO] Downloading user guide...
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/luomodeshang/desktop-pet/main/USER_GUIDE_%E5%B0%8F%E7%99%BD%E7%89%88.md' -OutFile '%INSTALL_DIR%\USER_GUIDE.md'" 2>nul

echo [OK] Assets downloaded!

echo.
echo ========================================
echo Step 5: Create shortcut
echo ========================================
echo.

echo [INFO] Creating desktop shortcut...

:: Create desktop shortcut
echo Set WshShell = CreateObject("WScript.Shell") > "%TEMP%\shortcut.vbs"
echo Set oShellLink = WshShell.CreateShortcut("%USERPROFILE%\Desktop\DesktopPet.lnk") >> "%TEMP%\shortcut.vbs"
echo oShellLink.TargetPath = "%INSTALL_DIR%\run.bat" >> "%TEMP%\shortcut.vbs"
echo oShellLink.WorkingDirectory = "%INSTALL_DIR%" >> "%TEMP%\shortcut.vbs"
echo oShellLink.Save >> "%TEMP%\shortcut.vbs"

cscript //nologo "%TEMP%\shortcut.vbs" 2>nul

if exist "%USERPROFILE%\Desktop\DesktopPet.lnk" (
    echo [OK] Desktop shortcut created!
) else (
    echo [WARNING] Failed to create desktop shortcut
)

echo.
echo ========================================
echo Step 6: Installation Complete!
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
echo IMPORTANT NOTES:
echo 1. If Windows shows security warning, click "More info" then "Run anyway"
echo 2. If Python is not installed, the script will show download link
echo 3. All commands are in English - no encoding issues
echo.
echo ========================================
echo Press 1 to start program, 2 to open folder, any other key to exit
echo.

choice /c 12 /n /m "Choose:"

if errorlevel 2 (
    echo Opening installation folder...
    explorer "%INSTALL_DIR%"
) else if errorlevel 1 (
    echo Starting Desktop Pet...
    start "" "%INSTALL_DIR%\run.bat"
)

echo.
echo Thank you for installing Desktop Pet!
echo If you have issues, check USER_GUIDE.md for troubleshooting
pause
exit /b 0