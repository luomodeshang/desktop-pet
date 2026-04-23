@echo off
chcp 65001 >nul
title Desktop Pet
color 0A

echo ========================================
echo     Desktop Pet - EXE Version
echo ========================================
echo.

:: Check if EXE exists
if not exist "DesktopPet.exe" (
    echo [ERROR] DesktopPet.exe not found!
    echo.
    echo Please download DesktopPet.exe from:
    echo https://github.com/luomodeshang/desktop-pet/releases
    echo.
    echo Or run the installer again.
    echo.
    pause
    exit /b 1
)

echo Starting Desktop Pet...
echo.
echo First run: Select a photo to create your pet
echo.
echo Controls:
echo - Right-click pet: Feed food
echo - Left-click pet: Trigger actions
echo - Drag: Move pet around
echo.
echo IMPORTANT: If Windows shows security warning:
echo 1. Click "More info"
echo 2. Click "Run anyway"
echo.
echo Press Ctrl+C to exit
echo ========================================
echo.

DesktopPet.exe

echo.
echo Desktop Pet closed.
pause