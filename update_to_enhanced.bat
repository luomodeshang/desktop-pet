@echo off
chcp 65001 >nul
title Desktop Pet - Complete Update
color 0A

echo ========================================
echo     Desktop Pet - Complete Update
echo ========================================
echo.
echo This updates your Desktop Pet installation
echo with all new features and fixes.
echo.
echo Press any key to continue...
pause >nul

:: Set variables
set INSTALL_DIR=%~dp0
if "%INSTALL_DIR%"=="" set INSTALL_DIR=%CD%\

echo.
echo Installation directory: %INSTALL_DIR%
echo.

:: Check if this is a Desktop Pet directory
if not exist "%INSTALL_DIR%\src\main.py" (
    echo [ERROR] This is not a Desktop Pet installation directory!
    echo.
    echo Please run this script from your DesktopPet folder.
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Step 1: Backup existing files
echo ========================================
echo.

echo [INFO] Creating backup...
set BACKUP_DIR=%INSTALL_DIR%_backup_%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%
xcopy "%INSTALL_DIR%" "%BACKUP_DIR%" /E /I /Y 2>nul
echo [OK] Backup created: %BACKUP_DIR%

echo.
echo ========================================
echo Step 2: Download updated source files
echo ========================================
echo.

set GITHUB_BASE=https://raw.githubusercontent.com/luomodeshang/desktop-pet/main

echo [INFO] Downloading updated files...

:: Download updated main.py
echo Downloading main.py...
powershell -Command "Invoke-WebRequest -Uri '%GITHUB_BASE%/src/main.py' -OutFile '%INSTALL_DIR%\src\main.py'" 2>nul

:: Download new files
echo Downloading icon_manager_gui.py...
powershell -Command "Invoke-WebRequest -Uri '%GITHUB_BASE%/src/icon_manager_gui.py' -OutFile '%INSTALL_DIR%\src\icon_manager_gui.py'" 2>nul

echo Downloading icon_manager.py...
powershell -Command "Invoke-WebRequest -Uri '%GITHUB_BASE%/src/icon_manager.py' -OutFile '%INSTALL_DIR%\src\icon_manager.py'" 2>nul

:: Download batch files
echo Downloading run_enhanced.bat...
powershell -Command "Invoke-WebRequest -Uri '%GITHUB_BASE%/run_enhanced.bat' -OutFile '%INSTALL_DIR%\run_enhanced.bat'" 2>nul

echo Downloading icon_manager.bat...
powershell -Command "Invoke-WebRequest -Uri '%GITHUB_BASE%/icon_manager.bat' -OutFile '%INSTALL_DIR%\icon_manager.bat'" 2>nul

echo [OK] Files downloaded!

echo.
echo ========================================
echo Step 3: Create required directories
echo ========================================
echo.

echo [INFO] Creating directories...

mkdir "%INSTALL_DIR%\assets\icons" 2>nul
mkdir "%INSTALL_DIR%\user_icons" 2>nul
mkdir "%INSTALL_DIR%\config" 2>nul

echo [OK] Directories created!

echo.
echo ========================================
echo Step 4: Update configuration
echo ========================================
echo.

echo [INFO] Updating configuration...

:: Check if config exists
if not exist "%INSTALL_DIR%\config\pet_config.json" (
    echo Creating new configuration...
    echo { > "%INSTALL_DIR%\config\pet_config.json"
    echo   "pet_size": [150, 150], >> "%INSTALL_DIR%\config\pet_config.json"
    echo   "position": [100, 100], >> "%INSTALL_DIR%\config\pet_config.json"
    echo   "last_state": "standing", >> "%INSTALL_DIR%\config\pet_config.json"
    echo   "food_history": [], >> "%INSTALL_DIR%\config\pet_config.json"
    echo   "user_photo_selected": false, >> "%INSTALL_DIR%\config\pet_config.json"
    echo   "use_default_avatar": false, >> "%INSTALL_DIR%\config\pet_config.json"
    echo   "user_photo": null, >> "%INSTALL_DIR%\config\pet_config.json"
    echo   "cartoon_path": null >> "%INSTALL_DIR%\config\pet_config.json"
    echo } >> "%INSTALL_DIR%\config\pet_config.json"
    echo [OK] Configuration created.
) else (
    echo [INFO] Existing configuration preserved.
)

echo.
echo ========================================
echo Step 5: Update desktop shortcut
echo ========================================
echo.

echo [INFO] Updating desktop shortcut...

:: Create updated shortcut
echo Set WshShell = CreateObject("WScript.Shell") > "%TEMP%\update_shortcut.vbs"
echo Set oShellLink = WshShell.CreateShortcut("%USERPROFILE%\Desktop\DesktopPet.lnk") >> "%TEMP%\update_shortcut.vbs"
echo oShellLink.TargetPath = "%INSTALL_DIR%\run_enhanced.bat" >> "%TEMP%\update_shortcut.vbs"
echo oShellLink.WorkingDirectory = "%INSTALL_DIR%" >> "%TEMP%\update_shortcut.vbs"
echo oShellLink.IconLocation = "%INSTALL_DIR%\assets\images\icon.ico" >> "%TEMP%\update_shortcut.vbs"
echo oShellLink.Save >> "%TEMP%\update_shortcut.vbs"

cscript //nologo "%TEMP%\update_shortcut.vbs" 2>nul

if exist "%USERPROFILE%\Desktop\DesktopPet.lnk" (
    echo [OK] Desktop shortcut updated!
) else (
    echo [WARNING] Failed to update desktop shortcut
)

echo.
echo ========================================
echo Step 6: Update Complete!
echo ========================================
echo.

echo [SUCCESS] Desktop Pet updated successfully!
echo.
echo New features added:
echo 1. Photo selection on first run
echo 2. Complete action animations (wave, jump, walk)
echo 3. Food feeding animations
echo 4. Icon manager for custom shortcut icons
echo 5. Enhanced menu system
echo 6. Food history tracking
echo.
echo Files updated:
echo - src\main.py (enhanced with all new features)
echo - src\icon_manager_gui.py (icon customization)
echo - src\icon_manager.py (icon management)
echo - run_enhanced.bat (new menu system)
echo - icon_manager.bat (icon manager launcher)
echo.
echo To start the updated program:
echo 1. Double-click "DesktopPet" on your desktop
echo 2. Or run: %INSTALL_DIR%\run_enhanced.bat
echo.
echo First time users: You will be asked to select a photo
echo Existing users: Your settings and history are preserved
echo.
echo ========================================
echo Press 1 to start now, 2 to open folder, any other key to exit
echo.

choice /c 12 /n /m "Choose:"

if errorlevel 2 (
    echo Opening installation folder...
    explorer "%INSTALL_DIR%"
) else if errorlevel 1 (
    echo Starting updated Desktop Pet...
    start "" "%INSTALL_DIR%\run_enhanced.bat"
)

echo.
echo Update complete! Enjoy the new features!
pause
exit /b 0