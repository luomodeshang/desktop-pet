@echo off
chcp 65001 >nul
title Desktop Pet
color 0A

echo ========================================
echo     Desktop Pet
echo ========================================
echo.

:: Check Python
python --version 2>nul
if errorlevel 1 (
    echo [ERROR] Python not found or not in PATH!
    echo.
    echo Please install Python 3.10+ from:
    echo https://www.python.org/downloads/
    echo.
    echo IMPORTANT: During installation, CHECK "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo Python found: 
python --version
echo.

:: Check if required libraries are installed
echo Checking required libraries...
python -c "import PyQt5, PIL, cv2" 2>nul
if %errorLevel% neq 0 (
    echo [INFO] Installing required libraries...
    echo This may take a few minutes...
    echo.
    
    pip install PyQt5
    pip install Pillow
    pip install opencv-python
    
    echo.
    echo [OK] Libraries installed!
    echo.
)

echo.
echo ========================================
echo     Desktop Pet Menu
echo ========================================
echo.
echo 1. Start Desktop Pet
echo 2. Change Photo
echo 3. Icon Manager (Customize shortcut icon)
echo 4. View Food History
echo 5. Exit
echo.
choice /c 12345 /n /m "Choose option:"

if errorlevel 5 (
    echo Exiting...
    pause
    exit /b 0
) else if errorlevel 4 (
    echo Opening food history...
    python -c "
import json
import os
try:
    config_path = 'config/pet_config.json'
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        history = config.get('food_history', [])
        if history:
            print('Food History:')
            print('=' * 30)
            for item in history[-10:]:
                print(f\"{item['time']} - {item['food']}\")
        else:
            print('No food history yet.')
    else:
        print('No configuration file found.')
except Exception as e:
    print(f'Error: {e}')
"
    echo.
    pause
    goto :menu_restart
) else if errorlevel 3 (
    echo Starting Icon Manager...
    call icon_manager.bat
    goto :menu_restart
) else if errorlevel 2 (
    echo Opening photo selection...
    python -c "
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.main import cartoonize_photo
import tkinter as tk
from tkinter import filedialog, messagebox

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename(
    title='Select Photo',
    filetypes=[('Image files', '*.jpg *.jpeg *.png *.bmp *.gif')]
)

if file_path:
    cartoon_path = 'assets/images/user_pet.png'
    if cartoonize_photo(file_path, cartoon_path):
        messagebox.showinfo('Success', 'Photo changed successfully!')
        print('Photo changed. Restart the program to see changes.')
    else:
        messagebox.showerror('Error', 'Failed to process photo')
else:
    print('No photo selected.')
"
    echo.
    pause
    goto :menu_restart
) else if errorlevel 1 (
    echo Starting Desktop Pet...
    echo.
    echo First run: You will be asked to select a photo
    echo.
    echo Controls:
    echo - Right-click pet: Feed food (hamburger, fried chicken, luosifen)
    echo - Left-click pet: Trigger actions (wave, jump, walk)
    echo - Drag: Move pet around
    echo.
    echo System Tray: Right-click system tray icon for more options
    echo.
    echo Press Ctrl+C to exit
    echo ========================================
    echo.
    
    cd /d "%~dp0"
    python src\main.py
)

:menu_restart
echo.
echo Returning to menu...
timeout /t 2 >nul
call "%~f0"
exit /b 0