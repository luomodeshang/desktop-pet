@echo off
chcp 65001 >nul
title Desktop Pet EXE Downloader
color 0A

echo ========================================
echo     Desktop Pet - EXE Downloader
echo ========================================
echo.
echo This downloads DesktopPet.exe to your Desktop
echo.
echo Press any key to start...
pause >nul

set DEST=%USERPROFILE%\Desktop\DesktopPet.exe
set URL=https://github.com/luomodeshang/desktop-pet/releases/latest/download/DesktopPet.exe

echo.
echo Downloading DesktopPet.exe...
echo.

:: Try PowerShell first
echo Method 1: Using PowerShell...
powershell -Command "Invoke-WebRequest -Uri '%URL%' -OutFile '%DEST%'"

if exist "%DEST%" goto :success

:: Try curl
echo Method 2: Using curl...
curl -L -o "%DEST%" "%URL%"

if exist "%DEST%" goto :success

:: Try bitsadmin
echo Method 3: Using bitsadmin...
bitsadmin /transfer DesktopPetDownload /download /priority normal "%URL%" "%DEST%"

if exist "%DEST%" goto :success

echo.
echo [ERROR] Failed to download
echo Please download manually from:
echo https://github.com/luomodeshang/desktop-pet/releases
echo.
pause
start https://github.com/luomodeshang/desktop-pet/releases
exit /b 1

:success
echo.
echo [SUCCESS] DesktopPet.exe downloaded!
echo Location: %DEST%
echo.
echo To run: Double-click the file on your Desktop
echo.
echo NOTE: Windows may show a security warning
echo Click "More info" then "Run anyway"
echo.
echo Press any key to run the program...
pause >nul

start "" "%DEST%"
exit /b 0