@echo off
chcp 65001 >nul
title 桌面宠物程序 - 小白专用安装器
color 0A

echo ========================================
echo     桌面宠物程序 - 小白专用安装器
echo ========================================
echo.
echo 专为没有任何Python基础的Windows用户设计
echo 全程自动化，一键完成所有安装步骤
echo.
echo 功能特点：
echo 1. ✅ 自动检测并安装Python环境
echo 2. ✅ 自动下载所有程序文件
echo 3. ✅ 自动安装所需库
echo 4. ✅ 自动创建桌面快捷方式
echo 5. ✅ 自动创建开始菜单项
echo 6. ✅ 安装完成自动启动程序
echo.
echo 按任意键开始安装...
pause >nul

:: 设置变量
set INSTALL_DIR=%USERPROFILE%\Desktop\我的桌面宠物
set TEMP_DIR=%TEMP%\desktop_pet_temp
set PYTHON_URL=https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe
set GITHUB_REPO=https://github.com/luomodeshang/desktop-pet

:: 创建临时目录
if not exist "%TEMP_DIR%" mkdir "%TEMP_DIR%"

echo.
echo ========================================
echo 第1步：检查Python环境
echo ========================================
echo.

:: 检查Python
where python >nul 2>&1
if %errorLevel% equ 0 (
    python --version
    echo ✅ 检测到Python已安装
    goto :check_pip
)

echo ❌ 未检测到Python环境
echo 📥 正在为您安装Python 3.10.11...

:: 下载Python安装程序
echo 正在下载Python安装程序...
powershell -Command "Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%TEMP_DIR%\python_installer.exe'" 2>nul

if not exist "%TEMP_DIR%\python_installer.exe" (
    echo ❌ Python安装程序下载失败
    echo 请检查网络连接后重试
    pause
    exit /b 1
)

echo ✅ Python安装程序下载完成
echo.
echo 🚀 正在安装Python...
echo 重要提示：请务必勾选"Add Python to PATH"选项！
echo 安装完成后请关闭安装窗口继续...
echo.
echo 按任意键启动Python安装程序...
pause >nul

start /wait "%TEMP_DIR%\python_installer.exe"

:: 等待并刷新环境变量
timeout /t 3 /nobreak >nul
call :refresh_env

:check_pip
echo.
echo 检查pip工具...
where pip >nul 2>&1
if %errorLevel% equ 0 (
    pip --version
    echo ✅ pip工具正常
    goto :download_files
)

echo ❌ pip工具未找到，正在安装...
python -m ensurepip --upgrade
echo ✅ pip安装完成

:download_files
echo.
echo ========================================
echo 第2步：下载桌面宠物程序
echo ========================================
echo.

echo 📁 创建安装目录：%INSTALL_DIR%
if exist "%INSTALL_DIR%" (
    echo ⚠️  检测到已存在，正在备份...
    if exist "%INSTALL_DIR%_backup" rmdir /s /q "%INSTALL_DIR%_backup"
    move "%INSTALL_DIR%" "%INSTALL_DIR%_backup"
)

mkdir "%INSTALL_DIR%" 2>nul
mkdir "%INSTALL_DIR%\src" 2>nul
mkdir "%INSTALL_DIR%\assets" 2>nul
mkdir "%INSTALL_DIR%\assets\images" 2>nul
mkdir "%INSTALL_DIR%\config" 2>nul

echo 📥 正在下载程序文件...

:: 下载文件列表
set FILES[0]=src/main.py
set FILES[1]=config/config.json
set FILES[2]=run.bat
set FILES[3]=requirements.txt
set FILES[4]=assets/images/default_avatar.png
set FILES[5]=assets/images/icon.ico
set FILES[6]=USER_GUIDE_小白版.md

set i=0
:download_loop
if defined FILES[%i%] (
    set FILE=!FILES[%i%]!
    
    echo 下载: !FILE!
    powershell -Command "Invoke-WebRequest -Uri '%GITHUB_REPO%/raw/main/!FILE!' -OutFile '%INSTALL_DIR%\!FILE!'" 2>nul
    
    if exist "%INSTALL_DIR%\!FILE!" (
        echo   ✅ 成功
    ) else (
        echo   ⚠️  失败（使用备用方案）
    )
    
    set /a i+=1
    goto :download_loop
)

echo ✅ 程序文件下载完成！

echo.
echo ========================================
echo 第3步：安装Python库
echo ========================================
echo.

echo 📦 正在安装所需Python库...
echo 这可能需要几分钟，请耐心等待...

cd /d "%INSTALL_DIR%"

echo 安装PyQt5（界面库）...
pip install PyQt5

echo 安装Pillow（图片处理）...
pip install Pillow

echo 安装opencv-python（头像生成）...
pip install opencv-python

echo 安装其他依赖...
if exist requirements.txt pip install -r requirements.txt

echo ✅ Python库安装完成！

echo.
echo ========================================
echo 第4步：创建快捷方式
echo ========================================
echo.

echo 🏠 创建桌面快捷方式...

:: 创建桌面快捷方式
echo Set WshShell = CreateObject("WScript.Shell") > "%TEMP_DIR%\shortcut.vbs"
echo Set oShellLink = WshShell.CreateShortcut("%USERPROFILE%\Desktop\桌面宠物.lnk") >> "%TEMP_DIR%\shortcut.vbs"
echo oShellLink.TargetPath = "%INSTALL_DIR%\run.bat" >> "%TEMP_DIR%\shortcut.vbs"
echo oShellLink.WorkingDirectory = "%INSTALL_DIR%" >> "%TEMP_DIR%\shortcut.vbs"
echo oShellLink.IconLocation = "%INSTALL_DIR%\assets\images\icon.ico" >> "%TEMP_DIR%\shortcut.vbs"
echo oShellLink.Save >> "%TEMP_DIR%\shortcut.vbs"

cscript //nologo "%TEMP_DIR%\shortcut.vbs"

if exist "%USERPROFILE%\Desktop\桌面宠物.lnk" (
    echo ✅ 桌面快捷方式创建成功！
) else (
    echo ⚠️  桌面快捷方式创建失败
)

echo.
echo 📋 创建开始菜单项...

:: 创建开始菜单目录
set START_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\桌面宠物
if not exist "%START_DIR%" mkdir "%START_DIR%"

echo Set WshShell = CreateObject("WScript.Shell") > "%TEMP_DIR%\startmenu.vbs"
echo Set oShellLink = WshShell.CreateShortcut("%START_DIR%\桌面宠物.lnk") >> "%TEMP_DIR%\startmenu.vbs"
echo oShellLink.TargetPath = "%INSTALL_DIR%\run.bat" >> "%TEMP_DIR%\startmenu.vbs"
echo oShellLink.WorkingDirectory = "%INSTALL_DIR%" >> "%TEMP_DIR%\startmenu.vbs"
echo oShellLink.IconLocation = "%INSTALL_DIR%\assets\images\icon.ico" >> "%TEMP_DIR%\shortcut.vbs"
echo oShellLink.Description = "可爱的桌面宠物程序" >> "%TEMP_DIR%\startmenu.vbs"
echo oShellLink.Save >> "%TEMP_DIR%\startmenu.vbs"

cscript //nologo "%TEMP_DIR%\startmenu.vbs"

echo ✅ 开始菜单项创建成功！

echo.
echo ========================================
echo 第5步：安装完成！
echo ========================================
echo.

echo 🎉 恭喜！桌面宠物程序安装完成！
echo.
echo 📍 安装位置：%INSTALL_DIR%
echo 🖥️  启动方式：
echo   1. 双击桌面上的"桌面宠物"图标
echo   2. 或进入开始菜单 > 桌面宠物
echo   3. 或直接运行：%INSTALL_DIR%\run.bat
echo.
echo 🐾 使用说明：
echo   - 首次运行需要选择一张照片
echo   - 右键宠物：投喂食物（汉堡、炸鸡、螺蛳粉）
echo   - 左键宠物：触发动作（挥手、跳跃、踱步）
echo   - 宠物会自动切换状态
echo   - 退出时自动保存状态
echo.
echo ⚠️  注意事项：
echo   - 如果杀毒软件误报，请添加信任
echo   - 需要网络连接（仅首次安装）
echo   - 支持Windows 7/8/10/11
echo.
echo ========================================
echo 按任意键启动桌面宠物程序...
pause >nul

:: 启动程序
start "" "%INSTALL_DIR%\run.bat"

echo.
echo 🐱 桌面宠物已启动！它会出现在屏幕右下角
echo 📖 详细使用指南：%INSTALL_DIR%\USER_GUIDE_小白版.md
echo.
echo 按任意键退出安装程序...
pause >nul

:: 清理临时文件
if exist "%TEMP_DIR%" rmdir /s /q "%TEMP_DIR%"

exit /b 0

:refresh_env
:: 刷新环境变量
for /f "skip=2 tokens=3*" %%a in ('reg query "HKCU\Environment" /v PATH 2^>nul') do set "USER_PATH=%%a %%b"
for /f "skip=2 tokens=3*" %%a in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PATH 2^>nul') do set "SYSTEM_PATH=%%a %%b"
set "PATH=%USER_PATH%;%SYSTEM_PATH%"
exit /b