@echo off
chcp 65001 >nul
title 桌面宠物程序 - 一键获取器
color 0A

echo ========================================
echo     桌面宠物程序 - 一键获取器
echo ========================================
echo.
echo 最简单的获取方式！无需任何技术知识
echo 只需双击，程序自动完成所有步骤
echo.
echo 适合人群：
echo ✅ 完全不懂编程的小白用户
echo ✅ 没有Python环境的Windows用户
echo ✅ 不想折腾安装过程的用户
echo.
echo 按任意键开始...
pause >nul

:: 设置变量
set VERSION=1.0.6
set DOWNLOAD_URL=https://github.com/luomodeshang/desktop-pet/releases/download/v%VERSION%
set INSTALL_DIR=%USERPROFILE%\Desktop\桌面宠物
set TEMP_DIR=%TEMP%\pet_downloader

:: 创建目录
if not exist "%TEMP_DIR%" mkdir "%TEMP_DIR%"

echo.
echo ========================================
echo 第1步：检查现有版本
echo ========================================
echo.

if exist "%INSTALL_DIR%" (
    echo ⚠️  检测到已安装的桌面宠物
    echo 正在备份旧版本...
    set BACKUP_DIR=%INSTALL_DIR%_备份_%date:~0,4%%date:~5,2%%date:~8,2%
    if exist "%BACKUP_DIR%" rmdir /s /q "%BACKUP_DIR%"
    move "%INSTALL_DIR%" "%BACKUP_DIR%" 2>nul
    echo ✅ 旧版本已备份到：%BACKUP_DIR%
)

echo.
echo ========================================
echo 第2步：选择下载方式
echo ========================================
echo.

echo 请选择下载方式：
echo 1. 快速下载（推荐）- 下载预打包的完整程序
echo 2. 完整下载 - 下载所有文件并自动安装
echo 3. 仅下载EXE文件（如可用）
echo.
set /p CHOICE="请选择 (1/2/3): "

if "%CHOICE%"=="1" goto :quick_download
if "%CHOICE%"=="2" goto :full_download
if "%CHOICE%"=="3" goto :exe_only
echo ❌ 选择无效，使用快速下载
goto :quick_download

:quick_download
echo.
echo 📥 正在下载预打包程序...
echo 这包含所有必需文件，解压即可使用

:: 尝试下载预打包版本
set PACKAGE_FILE=DesktopPet_Windows_v%VERSION%.zip
echo 下载: %PACKAGE_FILE%

powershell -Command "Invoke-WebRequest -Uri '%DOWNLOAD_URL%/%PACKAGE_FILE%' -OutFile '%TEMP_DIR%\%PACKAGE_FILE%'" 2>nul

if exist "%TEMP_DIR%\%PACKAGE_FILE%" (
    echo ✅ 下载成功！
    echo.
    echo 📦 正在解压文件...
    
    :: 创建安装目录
    mkdir "%INSTALL_DIR%" 2>nul
    
    :: 解压文件
    powershell -Command "Expand-Archive -Path '%TEMP_DIR%\%PACKAGE_FILE%' -DestinationPath '%INSTALL_DIR%' -Force" 2>nul
    
    if exist "%INSTALL_DIR%\run.bat" (
        echo ✅ 解压完成！
        goto :create_shortcuts
    ) else (
        echo ⚠️  解压失败，尝试完整下载
        goto :full_download
    )
) else (
    echo ⚠️  预打包版本下载失败，尝试完整下载
    goto :full_download
)

:full_download
echo.
echo 📥 正在下载完整程序包...
echo 这需要一些时间，请耐心等待...

:: 创建目录结构
mkdir "%INSTALL_DIR%" 2>nul
mkdir "%INSTALL_DIR%\src" 2>nul
mkdir "%INSTALL_DIR%\assets" 2>nul
mkdir "%INSTALL_DIR%\assets\images" 2>nul
mkdir "%INSTALL_DIR%\config" 2>nul

:: 下载必要文件
echo 下载主程序...
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/luomodeshang/desktop-pet/main/src/main.py' -OutFile '%INSTALL_DIR%\src\main.py'" 2>nul

echo 下载配置文件...
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/luomodeshang/desktop-pet/main/config/config.json' -OutFile '%INSTALL_DIR%\config\config.json'" 2>nul

echo 下载运行脚本...
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/luomodeshang/desktop-pet/main/run.bat' -OutFile '%INSTALL_DIR%\run.bat'" 2>nul

echo 下载默认头像...
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/luomodeshang/desktop-pet/main/assets/images/default_avatar.png' -OutFile '%INSTALL_DIR%\assets\images\default_avatar.png'" 2>nul

echo 下载图标...
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/luomodeshang/desktop-pet/main/assets/images/icon.ico' -OutFile '%INSTALL_DIR%\assets\images\icon.ico'" 2>nul

echo 下载用户指南...
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/luomodeshang/desktop-pet/main/USER_GUIDE_小白版.md' -OutFile '%INSTALL_DIR%\USER_GUIDE_小白版.md'" 2>nul

echo ✅ 文件下载完成！

:: 检查是否安装了Python
where python >nul 2>&1
if %errorLevel% equ 0 (
    echo.
    echo 🐍 检测到Python环境
    echo 📦 正在安装所需库...
    
    cd /d "%INSTALL_DIR%"
    
    echo 安装PyQt5...
    pip install PyQt5 2>nul
    
    echo 安装Pillow...
    pip install Pillow 2>nul
    
    echo ✅ 库安装完成！
) else (
    echo.
    echo ⚠️  未检测到Python环境
    echo 程序需要Python才能运行
    echo 正在为您安装Python...
    
    call :install_python
)

goto :create_shortcuts

:exe_only
echo.
echo ⚠️  EXE文件正在构建中，暂时不可用
echo 请使用其他下载方式
echo 按任意键返回选择...
pause >nul
goto :full_download

:create_shortcuts
echo.
echo ========================================
echo 第3步：创建快捷方式
echo ========================================
echo.

echo 🏠 创建桌面快捷方式...

:: 创建快捷方式VBS脚本
echo Set WshShell = CreateObject("WScript.Shell") > "%TEMP_DIR%\create_shortcut.vbs"
echo strDesktop = WshShell.SpecialFolders("Desktop") >> "%TEMP_DIR%\create_shortcut.vbs"
echo Set oShellLink = WshShell.CreateShortcut(strDesktop ^& "\桌面宠物.lnk") >> "%TEMP_DIR%\create_shortcut.vbs"
echo oShellLink.TargetPath = "%INSTALL_DIR%\run.bat" >> "%TEMP_DIR%\create_shortcut.vbs"
echo oShellLink.WorkingDirectory = "%INSTALL_DIR%" >> "%TEMP_DIR%\create_shortcut.vbs"
echo oShellLink.IconLocation = "%INSTALL_DIR%\assets\images\icon.ico" >> "%TEMP_DIR%\create_shortcut.vbs"
echo oShellLink.Save >> "%TEMP_DIR%\create_shortcut.vbs"

cscript //nologo "%TEMP_DIR%\create_shortcut.vbs"

if exist "%USERPROFILE%\Desktop\桌面宠物.lnk" (
    echo ✅ 桌面快捷方式创建成功！
) else (
    echo ⚠️  快捷方式创建失败，但程序仍可运行
)

echo.
echo ========================================
echo 第4步：安装完成！
echo ========================================
echo.

echo 🎉 桌面宠物程序获取完成！
echo.
echo 📍 程序位置：%INSTALL_DIR%
echo 🖥️  启动方式：
echo   1. 双击桌面上的"桌面宠物"图标
echo   2. 或运行：%INSTALL_DIR%\run.bat
echo.
echo 🐾 快速开始：
echo   1. 首次运行选择一张照片
echo   2. 右键宠物投喂食物
echo   3. 左键宠物触发动作
echo   4. 宠物会自动活动
echo.
echo 📖 详细指南：%INSTALL_DIR%\USER_GUIDE_小白版.md
echo 🔗 项目主页：https://github.com/luomodeshang/desktop-pet
echo.
echo ========================================
echo 按 1 启动程序，按 2 打开安装目录，其他键退出
choice /c 12 /n /m "请选择:"

if errorlevel 2 (
    echo 📂 打开安装目录...
    explorer "%INSTALL_DIR%"
) else if errorlevel 1 (
    echo 🚀 启动桌面宠物...
    start "" "%INSTALL_DIR%\run.bat"
)

:: 清理临时文件
if exist "%TEMP_DIR%" rmdir /s /q "%TEMP_DIR%"

echo.
echo 感谢使用！按任意键退出...
pause >nul
exit /b 0

:install_python
:: 安装Python
echo 📥 下载Python安装程序...
set PYTHON_URL=https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe
powershell -Command "Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%TEMP_DIR%\python.exe'" 2>nul

if not exist "%TEMP_DIR%\python.exe" (
    echo ❌ Python下载失败
    echo 请手动安装Python：https://www.python.org/downloads/
    echo 安装后重新运行此程序
    pause
    exit /b 1
)

echo 🚀 正在安装Python...
echo 重要：请务必勾选"Add Python to PATH"！
echo 安装完成后关闭窗口继续...
echo 按任意键启动安装...
pause >nul

start /wait "%TEMP_DIR%\python.exe"

:: 等待安装完成
timeout /t 5 /nobreak >nul

:: 刷新环境变量
call :refresh_path

:: 验证安装
where python >nul 2>&1
if %errorLevel% equ 0 (
    echo ✅ Python安装成功！
    
    :: 安装必要库
    cd /d "%INSTALL_DIR%"
    echo 📦 安装程序库...
    pip install PyQt5 Pillow 2>nul
    echo ✅ 库安装完成！
) else (
    echo ⚠️  Python安装可能未完成
    echo 请手动运行程序安装Python库
)

exit /b

:refresh_path
:: 刷新环境变量
for /f "skip=2 tokens=3*" %%a in ('reg query "HKCU\Environment" /v PATH 2^>nul') do set "USER_PATH=%%a %%b"
for /f "skip=2 tokens=3*" %%a in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PATH 2^>nul') do set "SYSTEM_PATH=%%a %%b"
set "PATH=%USER_PATH%;%SYSTEM_PATH%"
exit /b