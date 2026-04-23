@echo off
chcp 65001 >nul
title Desktop Pet - ZIP Downloader
color 0A

echo ========================================
echo     Desktop Pet - ZIP Downloader
echo ========================================
echo.
echo This downloads the complete project as ZIP
echo Then extracts and sets up everything
echo.
echo Press any key to continue...
pause >nul

:: Set variables
set INSTALL_DIR=%USERPROFILE%\Desktop\DesktopPet
set ZIP_URL=https://github.com/luomodeshang/desktop-pet/archive/refs/heads/main.zip
set TEMP_ZIP=%TEMP%\desktop-pet.zip

echo.
echo ========================================
echo Step 1: Download ZIP file
echo ========================================
echo.

echo [INFO] Downloading project ZIP...
echo This may take a minute...

:: Download ZIP file
powershell -Command "Invoke-WebRequest -Uri '%ZIP_URL%' -OutFile '%TEMP_ZIP%'" 2>nul

if not exist "%TEMP_ZIP%" (
    echo [ERROR] Failed to download ZIP file
    echo.
    echo Please download manually from:
    echo https://github.com/luomodeshang/desktop-pet
    echo Click "Code" -> "Download ZIP"
    echo.
    pause
    exit /b 1
)

echo [OK] ZIP file downloaded!

echo.
echo ========================================
echo Step 2: Extract files
echo ========================================
echo.

echo [INFO] Extracting files...

:: Create temp extraction directory
set TEMP_EXTRACT=%TEMP%\desktop-pet-extract
if exist "%TEMP_EXTRACT%" rmdir /s /q "%TEMP_EXTRACT%"
mkdir "%TEMP_EXTRACT%"

:: Extract ZIP
powershell -Command "Expand-Archive -Path '%TEMP_ZIP%' -DestinationPath '%TEMP_EXTRACT%'" 2>nul

if not exist "%TEMP_EXTRACT%\desktop-pet-main" (
    echo [ERROR] Failed to extract ZIP
    echo.
    echo Please extract manually:
    echo 1. Open %TEMP_ZIP%
    echo 2. Extract to %INSTALL_DIR%
    echo.
    pause
    exit /b 1
)

echo [OK] Files extracted!

echo.
echo ========================================
echo Step 3: Copy to installation directory
echo ========================================
echo.

if exist "%INSTALL_DIR%" (
    echo [INFO] Backup existing installation...
    if exist "%INSTALL_DIR%_backup" rmdir /s /q "%INSTALL_DIR%_backup"
    move "%INSTALL_DIR%" "%INSTALL_DIR%_backup" 2>nul
)

echo [INFO] Copying files to %INSTALL_DIR%...
xcopy "%TEMP_EXTRACT%\desktop-pet-main\*" "%INSTALL_DIR%" /E /I /Y 2>nul

echo [OK] Files copied!

echo.
echo ========================================
echo Step 4: Clean up and create run script
echo ========================================
echo.

echo [INFO] Cleaning up temporary files...
if exist "%TEMP_ZIP%" del "%TEMP_ZIP%"
if exist "%TEMP_EXTRACT%" rmdir /s /q "%TEMP_EXTRACT%"

echo [INFO] Creating simple run script...

:: Create simple run script
echo @echo off > "%INSTALL_DIR%\run_simple.bat"
echo chcp 65001 ^>nul >> "%INSTALL_DIR%\run_simple.bat"
echo title Desktop Pet >> "%INSTALL_DIR%\run_simple.bat"
echo. >> "%INSTALL_DIR%\run_simple.bat"
echo echo ======================================== >> "%INSTALL_DIR%\run_simple.bat"
echo echo     Desktop Pet >> "%INSTALL_DIR%\run_simple.bat"
echo echo ======================================== >> "%INSTALL_DIR%\run_simple.bat"
echo echo. >> "%INSTALL_DIR%\run_simple.bat"
echo. >> "%INSTALL_DIR%\run_simple.bat"
echo :: Check Python >> "%INSTALL_DIR%\run_simple.bat"
echo python --version 2^>nul >> "%INSTALL_DIR%\run_simple.bat"
echo if errorlevel 1 ( >> "%INSTALL_DIR%\run_simple.bat"
echo     echo ERROR: Python not found! >> "%INSTALL_DIR%\run_simple.bat"
echo     echo. >> "%INSTALL_DIR%\run_simple.bat"
echo     echo Install Python from: https://www.python.org/downloads/ >> "%INSTALL_DIR%\run_simple.bat"
echo     echo Make sure to check "Add Python to PATH" >> "%INSTALL_DIR%\run_simple.bat"
echo     pause >> "%INSTALL_DIR%\run_simple.bat"
echo     exit /b 1 >> "%INSTALL_DIR%\run_simple.bat"
echo ) >> "%INSTALL_DIR%\run_simple.bat"
echo. >> "%INSTALL_DIR%\run_simple.bat"
echo :: Install requirements >> "%INSTALL_DIR%\run_simple.bat"
echo echo Installing required libraries... >> "%INSTALL_DIR%\run_simple.bat"
echo pip install -r requirements.txt >> "%INSTALL_DIR%\run_simple.bat"
echo. >> "%INSTALL_DIR%\run_simple.bat"
echo :: Run program >> "%INSTALL_DIR%\run_simple.bat"
echo echo Starting Desktop Pet... >> "%INSTALL_DIR%\run_simple.bat"
echo python src\main.py >> "%INSTALL_DIR%\run_simple.bat"
echo. >> "%INSTALL_DIR%\run_simple.bat"
echo echo Program closed. >> "%INSTALL_DIR%\run_simple.bat"
echo pause >> "%INSTALL_DIR%\run_simple.bat"

echo [OK] Simple run script created!

echo.
echo ========================================
echo Step 5: Create shortcut
echo ========================================
echo.

echo [INFO] Creating desktop shortcut...

:: Create desktop shortcut
echo Set WshShell = CreateObject("WScript.Shell") > "%TEMP%\shortcut.vbs"
echo Set oShellLink = WshShell.CreateShortcut("%USERPROFILE%\Desktop\DesktopPet.lnk") >> "%TEMP%\shortcut.vbs"
echo oShellLink.TargetPath = "%INSTALL_DIR%\run_simple.bat" >> "%TEMP%\shortcut.vbs"
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
echo Files included:
echo - Complete source code
echo - All assets and images
echo - Configuration files
echo - User guides
echo.
echo To start the program:
echo 1. Double-click "DesktopPet" on your desktop
echo 2. Or run: %INSTALL_DIR%\run_simple.bat
echo.
echo First time setup:
echo 1. Python will be checked
echo 2. Required libraries will be installed
echo 3. Program will start
echo.
echo ========================================
echo Press 1 to verify files, 2 to start program, any other key to exit
echo.

choice /c 12 /n /m "Choose:"

if errorlevel 2 (
    echo Starting Desktop Pet...
    start "" "%INSTALL_DIR%\run_simple.bat"
) else if errorlevel 1 (
    echo Verifying files...
    echo.
    echo Directory: %INSTALL_DIR%
    dir "%INSTALL_DIR%"
    echo.
    echo Press any key to continue...
    pause >nul
)

echo.
echo Installation complete!
echo If you have issues, make sure Python is installed and in PATH.
pause
exit /b 0