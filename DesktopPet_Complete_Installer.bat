@echo off
chcp 65001 >nul
title Desktop Pet Complete Installer
color 0A

echo ========================================
echo     Desktop Pet - Complete Installer
echo ========================================
echo.
echo This installer downloads ALL required files
echo Includes source code, assets, and configs
echo.
echo Press any key to continue...
pause >nul

:: Set variables
set INSTALL_DIR=%USERPROFILE%\Desktop\DesktopPet
set GITHUB_BASE=https://raw.githubusercontent.com/luomodeshang/desktop-pet/main

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
mkdir "%INSTALL_DIR%\src" 2>nul
mkdir "%INSTALL_DIR%\assets" 2>nul
mkdir "%INSTALL_DIR%\assets\images" 2>nul
mkdir "%INSTALL_DIR%\config" 2>nul

echo [OK] Folder structure created: %INSTALL_DIR%

echo.
echo ========================================
echo Step 2: Download source code files
echo ========================================
echo.

echo [INFO] Downloading source code files...

:: Download main Python files
echo Downloading main.py...
powershell -Command "Invoke-WebRequest -Uri '%GITHUB_BASE%/src/main.py' -OutFile '%INSTALL_DIR%\src\main.py'" 2>nul

echo Downloading pet.py...
powershell -Command "Invoke-WebRequest -Uri '%GITHUB_BASE%/src/pet.py' -OutFile '%INSTALL_DIR%\src\pet.py'" 2>nul

echo Downloading ui.py...
powershell -Command "Invoke-WebRequest -Uri '%GITHUB_BASE%/src/ui.py' -OutFile '%INSTALL_DIR%\src\ui.py'" 2>nul

echo Downloading utils.py...
powershell -Command "Invoke-WebRequest -Uri '%GITHUB_BASE%/src/utils.py' -OutFile '%INSTALL_DIR%\src\utils.py'" 2>nul

echo Downloading requirements.txt...
powershell -Command "Invoke-WebRequest -Uri '%GITHUB_BASE%/requirements.txt' -OutFile '%INSTALL_DIR%\requirements.txt'" 2>nul

:: Check if files were downloaded
if exist "%INSTALL_DIR%\src\main.py" (
    echo [OK] Source code downloaded!
) else (
    echo [WARNING] Some files may not have downloaded
    echo You may need to download them manually
)

echo.
echo ========================================
echo Step 3: Download config files
echo ========================================
echo.

echo [INFO] Downloading configuration files...

echo Downloading config.json...
powershell -Command "Invoke-WebRequest -Uri '%GITHUB_BASE%/config/config.json' -OutFile '%INSTALL_DIR%\config\config.json'" 2>nul

echo Downloading food_config.json...
powershell -Command "Invoke-WebRequest -Uri '%GITHUB_BASE%/config/food_config.json' -OutFile '%INSTALL_DIR%\config\food_config.json'" 2>nul

echo Downloading action_config.json...
powershell -Command "Invoke-WebRequest -Uri '%GITHUB_BASE%/config/action_config.json' -OutFile '%INSTALL_DIR%\config\action_config.json'" 2>nul

echo [OK] Config files downloaded!

echo.
echo ========================================
echo Step 4: Download assets
echo ========================================
echo.

echo [INFO] Downloading assets...

echo Downloading default avatar...
powershell -Command "Invoke-WebRequest -Uri '%GITHUB_BASE%/assets/images/default_avatar.png' -OutFile '%INSTALL_DIR%\assets\images\default_avatar.png'" 2>nul

echo Downloading icon...
powershell -Command "Invoke-WebRequest -Uri '%GITHUB_BASE%/assets/images/icon.ico' -OutFile '%INSTALL_DIR%\assets\images\icon.ico'" 2>nul

echo Downloading hamburger.png...
powershell -Command "Invoke-WebRequest -Uri '%GITHUB_BASE%/assets/images/hamburger.png' -OutFile '%INSTALL_DIR%\assets\images\hamburger.png'" 2>nul

echo Downloading fried_chicken.png...
powershell -Command "Invoke-WebRequest -Uri '%GITHUB_BASE%/assets/images/fried_chicken.png' -OutFile '%INSTALL_DIR%\assets\images\fried_chicken.png'" 2>nul

echo Downloading luosifen.png...
powershell -Command "Invoke-WebRequest -Uri '%GITHUB_BASE%/assets/images/luosifen.png' -OutFile '%INSTALL_DIR%\assets\images\luosifen.png'" 2>nul

echo [OK] Assets downloaded!

echo.
echo ========================================
echo Step 5: Create run script
echo ========================================
echo.

echo [INFO] Creating run script...

:: Create complete run script
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
echo :: Check Python >> "%INSTALL_DIR%\run.bat"
echo where python ^>nul 2^>^&1 >> "%INSTALL_DIR%\run.bat"
echo if %%errorLevel%% neq 0 ( >> "%INSTALL_DIR%\run.bat"
echo     echo [ERROR] Python not found! >> "%INSTALL_DIR%\run.bat"
echo     echo. >> "%INSTALL_DIR%\run.bat"
echo     echo Please install Python 3.10+ from: >> "%INSTALL_DIR%\run.bat"
echo     echo https://www.python.org/downloads/ >> "%INSTALL_DIR%\run.bat"
echo     echo. >> "%INSTALL_DIR%\run.bat"
echo     echo IMPORTANT: Check "Add Python to PATH" during installation >> "%INSTALL_DIR%\run.bat"
echo     echo. >> "%INSTALL_DIR%\run.bat"
echo     pause >> "%INSTALL_DIR%\run.bat"
echo     exit /b 1 >> "%INSTALL_DIR%\run.bat"
echo ) >> "%INSTALL_DIR%\run.bat"
echo. >> "%INSTALL_DIR%\run.bat"
echo python --version >> "%INSTALL_DIR%\run.bat"
echo. >> "%INSTALL_DIR%\run.bat"
echo :: Check if required libraries are installed >> "%INSTALL_DIR%\run.bat"
echo echo Checking required libraries... >> "%INSTALL_DIR%\run.bat"
echo python -c "import PyQt5, PIL, cv2" 2^>nul >> "%INSTALL_DIR%\run.bat"
echo if %%errorLevel%% neq 0 ( >> "%INSTALL_DIR%\run.bat"
echo     echo [INFO] Installing required libraries... >> "%INSTALL_DIR%\run.bat"
echo     echo This may take a few minutes... >> "%INSTALL_DIR%\run.bat"
echo     echo. >> "%INSTALL_DIR%\run.bat"
echo     pip install PyQt5 >> "%INSTALL_DIR%\run.bat"
echo     pip install Pillow >> "%INSTALL_DIR%\run.bat"
echo     pip install opencv-python >> "%INSTALL_DIR%\run.bat"
echo     echo. >> "%INSTALL_DIR%\run.bat"
echo     echo [OK] Libraries installed! >> "%INSTALL_DIR%\run.bat"
echo     echo. >> "%INSTALL_DIR%\run.bat"
echo ) >> "%INSTALL_DIR%\run.bat"
echo. >> "%INSTALL_DIR%\run.bat"
echo :: Run the program >> "%INSTALL_DIR%\run.bat"
echo echo Starting Desktop Pet... >> "%INSTALL_DIR%\run.bat"
echo echo. >> "%INSTALL_DIR%\run.bat"
echo echo First run: Select a photo to create your pet >> "%INSTALL_DIR%\run.bat"
echo echo. >> "%INSTALL_DIR%\run.bat"
echo echo Controls: >> "%INSTALL_DIR%\run.bat"
echo echo - Right-click pet: Feed food ^(hamburger, fried chicken, luosifen^) >> "%INSTALL_DIR%\run.bat"
echo echo - Left-click pet: Trigger actions ^(wave, jump, walk^) >> "%INSTALL_DIR%\run.bat"
echo echo - Drag: Move pet around >> "%INSTALL_DIR%\run.bat"
echo echo. >> "%INSTALL_DIR%\run.bat"
echo echo Press Ctrl+C to exit >> "%INSTALL_DIR%\run.bat"
echo echo ======================================== >> "%INSTALL_DIR%\run.bat"
echo echo. >> "%INSTALL_DIR%\run.bat"
echo. >> "%INSTALL_DIR%\run.bat"
echo cd /d "%%~dp0" >> "%INSTALL_DIR%\run.bat"
echo python src\main.py >> "%INSTALL_DIR%\run.bat"
echo. >> "%INSTALL_DIR%\run.bat"
echo echo. >> "%INSTALL_DIR%\run.bat"
echo echo Desktop Pet closed. >> "%INSTALL_DIR%\run.bat"
echo pause >> "%INSTALL_DIR%\run.bat"

echo [OK] Run script created!

echo.
echo ========================================
echo Step 6: Create shortcut
echo ========================================
echo.

echo [INFO] Creating desktop shortcut...

:: Create desktop shortcut
echo Set WshShell = CreateObject("WScript.Shell") > "%TEMP%\shortcut.vbs"
echo Set oShellLink = WshShell.CreateShortcut("%USERPROFILE%\Desktop\DesktopPet.lnk") >> "%TEMP%\shortcut.vbs"
echo oShellLink.TargetPath = "%INSTALL_DIR%\run.bat" >> "%TEMP%\shortcut.vbs"
echo oShellLink.WorkingDirectory = "%INSTALL_DIR%" >> "%TEMP%\shortcut.vbs"
echo oShellLink.IconLocation = "%INSTALL_DIR%\assets\images\icon.ico" >> "%INSTALL_DIR%\shortcut.vbs"
echo oShellLink.Save >> "%TEMP%\shortcut.vbs"

cscript //nologo "%TEMP%\shortcut.vbs" 2>nul

if exist "%USERPROFILE%\Desktop\DesktopPet.lnk" (
    echo [OK] Desktop shortcut created!
) else (
    echo [WARNING] Failed to create desktop shortcut
)

echo.
echo ========================================
echo Step 7: Installation Complete!
echo ========================================
echo.

echo [SUCCESS] Desktop Pet installed successfully!
echo.
echo Files downloaded:
echo - Source code: main.py, pet.py, ui.py, utils.py
echo - Config files: config.json, food_config.json, action_config.json
echo - Assets: default_avatar.png, icon.ico, food images
echo - Requirements: requirements.txt
echo.
echo Installation location: %INSTALL_DIR%
echo.
echo To start the program:
echo 1. Double-click "DesktopPet" on your desktop
echo 2. Or run: %INSTALL_DIR%\run.bat
echo.
echo IMPORTANT: If Python is not installed:
echo 1. Download from https://www.python.org/downloads/
echo 2. Install Python 3.10+
echo 3. CHECK "Add Python to PATH" during installation
echo.
echo ========================================
echo Press 1 to check installation, 2 to open folder, any other key to exit
echo.

choice /c 12 /n /m "Choose:"

if errorlevel 2 (
    echo Opening installation folder...
    explorer "%INSTALL_DIR%"
) else if errorlevel 1 (
    echo Checking installation...
    echo.
    echo Files in installation directory:
    dir "%INSTALL_DIR%"
    echo.
    echo Files in src directory:
    dir "%INSTALL_DIR%\src"
    echo.
    echo Press any key to continue...
    pause >nul
)

echo.
echo Thank you for installing Desktop Pet!
echo If you have issues:
echo 1. Make sure Python is installed and in PATH
echo 2. Run the program again - it will install required libraries
echo 3. Check %INSTALL_DIR%\USER_GUIDE.md for help
pause
exit /b 0