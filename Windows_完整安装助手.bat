@echo off
chcp 65001 >nul
title 桌面宠物程序 - Windows一键安装助手
color 0A

echo ========================================
echo     桌面宠物程序 Windows一键安装助手
echo ========================================
echo.
echo 此脚本将自动为您安装桌面宠物程序
echo 包括：Python环境、所需库、程序文件
echo.
echo 目标用户：没有任何Python基础的Windows用户
echo.
echo 按任意键开始安装，或按 Ctrl+C 取消...
pause >nul

:: 检查是否以管理员身份运行
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo.
    echo ⚠️  检测到未以管理员身份运行
    echo 某些操作可能需要管理员权限
    echo 建议右键点击此文件，选择"以管理员身份运行"
    echo.
    echo 按任意键继续（可能遇到权限问题）...
    pause >nul
)

echo.
echo ========================================
echo 步骤1：检查系统环境
echo ========================================
echo.

:: 检查Python是否已安装
where python >nul 2>&1
if %errorLevel% equ 0 (
    python --version
    echo ✅ Python已安装
    set PYTHON_INSTALLED=1
) else (
    echo ❌ Python未安装
    set PYTHON_INSTALLED=0
)

:: 检查pip是否可用
where pip >nul 2>&1
if %errorLevel% equ 0 (
    pip --version
    echo ✅ pip已安装
    set PIP_INSTALLED=1
) else (
    echo ❌ pip未安装
    set PIP_INSTALLED=0
)

echo.
echo ========================================
echo 步骤2：安装Python（如需要）
echo ========================================
echo.

if %PYTHON_INSTALLED% equ 0 (
    echo 📥 正在下载Python安装程序...
    
    :: 创建临时目录
    set TEMP_DIR=%TEMP%\desktop_pet_install
    if not exist "%TEMP_DIR%" mkdir "%TEMP_DIR%"
    
    :: 下载Python安装程序
    echo 正在从Python官网下载安装程序...
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe' -OutFile '%TEMP_DIR%\python-installer.exe'"
    
    if exist "%TEMP_DIR%\python-installer.exe" (
        echo ✅ Python安装程序下载完成
        echo.
        echo 🚀 正在安装Python 3.10.11...
        echo 请按照安装向导完成安装
        echo 重要：请务必勾选"Add Python to PATH"选项！
        echo.
        echo 按任意键启动Python安装程序...
        pause >nul
        
        start /wait "%TEMP_DIR%\python-installer.exe"
        
        :: 等待安装完成并刷新环境变量
        timeout /t 5 /nobreak >nul
        call :refresh_path
        
        :: 验证安装
        where python >nul 2>&1
        if %errorLevel% equ 0 (
            python --version
            echo ✅ Python安装成功！
            set PYTHON_INSTALLED=1
        ) else (
            echo ❌ Python安装失败，请手动安装
            echo 访问：https://www.python.org/downloads/
            goto :error_exit
        )
    ) else (
        echo ❌ Python安装程序下载失败
        echo 请手动下载并安装Python
        echo 访问：https://www.python.org/downloads/
        goto :error_exit
    )
) else (
    echo ⏭️  Python已安装，跳过此步骤
)

echo.
echo ========================================
echo 步骤3：安装pip（如需要）
echo ========================================
echo.

if %PIP_INSTALLED% equ 0 (
    echo 📦 正在安装pip...
    
    :: 下载get-pip.py
    echo 正在下载pip安装脚本...
    powershell -Command "Invoke-WebRequest -Uri 'https://bootstrap.pypa.io/get-pip.py' -OutFile '%TEMP_DIR%\get-pip.py'"
    
    if exist "%TEMP_DIR%\get-pip.py" (
        python "%TEMP_DIR%\get-pip.py"
        
        :: 验证安装
        where pip >nul 2>&1
        if %errorLevel% equ 0 (
            pip --version
            echo ✅ pip安装成功！
            set PIP_INSTALLED=1
        ) else (
            echo ❌ pip安装失败
            goto :error_exit
        )
    ) else (
        echo ❌ pip安装脚本下载失败
        goto :error_exit
    )
) else (
    echo ⏭️  pip已安装，跳过此步骤
)

echo.
echo ========================================
echo 步骤4：下载桌面宠物程序
echo ========================================
echo.

:: 设置安装目录
set INSTALL_DIR=%USERPROFILE%\Desktop\DesktopPet
echo 安装目录：%INSTALL_DIR%

if exist "%INSTALL_DIR%" (
    echo ⚠️  检测到已存在安装目录
    echo 正在备份旧版本...
    if exist "%INSTALL_DIR%.backup" rmdir /s /q "%INSTALL_DIR%.backup"
    move "%INSTALL_DIR%" "%INSTALL_DIR%.backup"
    echo ✅ 旧版本已备份到：%INSTALL_DIR%.backup
)

echo.
echo 📥 正在下载桌面宠物程序...
echo 从GitHub下载最新版本...

:: 创建安装目录
mkdir "%INSTALL_DIR%" 2>nul
mkdir "%INSTALL_DIR%\src" 2>nul
mkdir "%INSTALL_DIR%\assets" 2>nul
mkdir "%INSTALL_DIR%\assets\images" 2>nul
mkdir "%INSTALL_DIR%\config" 2>nul

:: 下载主要文件
echo 下载程序文件...

:: 下载主程序
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/luomodeshang/desktop-pet/main/src/main.py' -OutFile '%INSTALL_DIR%\src\main.py'"

:: 下载配置文件
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/luomodeshang/desktop-pet/main/config/config.json' -OutFile '%INSTALL_DIR%\config\config.json'"

:: 下载运行脚本
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/luomodeshang/desktop-pet/main/run.bat' -OutFile '%INSTALL_DIR%\run.bat'"

:: 下载依赖文件
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/luomodeshang/desktop-pet/main/requirements.txt' -OutFile '%INSTALL_DIR%\requirements.txt'"

:: 下载默认头像
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/luomodeshang/desktop-pet/main/assets/images/default_avatar.png' -OutFile '%INSTALL_DIR%\assets\images\default_avatar.png'"

:: 下载图标
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/luomodeshang/desktop-pet/main/assets/images/icon.ico' -OutFile '%INSTALL_DIR%\assets\images\icon.ico'"

echo ✅ 程序文件下载完成！

echo.
echo ========================================
echo 步骤5：安装Python依赖库
echo ========================================
echo.

echo 📦 正在安装所需Python库...
echo 这可能需要几分钟时间，请耐心等待...

cd /d "%INSTALL_DIR%"
pip install --upgrade pip

:: 安装主要依赖
echo 安装PyQt5...
pip install PyQt5

echo 安装Pillow...
pip install Pillow

echo 安装opencv-python...
pip install opencv-python

:: 安装requirements.txt中的所有依赖
if exist requirements.txt (
    echo 安装其他依赖...
    pip install -r requirements.txt
)

echo ✅ Python依赖库安装完成！

echo.
echo ========================================
echo 步骤6：创建桌面快捷方式
echo ========================================
echo.

echo 🏠 正在创建桌面快捷方式...

set SHORTCUT_PATH=%USERPROFILE%\Desktop\桌面宠物.lnk
set TARGET_PATH=%INSTALL_DIR%\run.bat
set ICON_PATH=%INSTALL_DIR%\assets\images\icon.ico

:: 创建VBS脚本创建快捷方式
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP_DIR%\create_shortcut.vbs"
echo sLinkFile = "%SHORTCUT_PATH%" >> "%TEMP_DIR%\create_shortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP_DIR%\create_shortcut.vbs"
echo oLink.TargetPath = "%TARGET_PATH%" >> "%TEMP_DIR%\create_shortcut.vbs"
echo oLink.WorkingDirectory = "%INSTALL_DIR%" >> "%TEMP_DIR%\create_shortcut.vbs"
echo oLink.IconLocation = "%ICON_PATH%" >> "%TEMP_DIR%\create_shortcut.vbs"
echo oLink.Save >> "%TEMP_DIR%\create_shortcut.vbs"

cscript //nologo "%TEMP_DIR%\create_shortcut.vbs"

if exist "%SHORTCUT_PATH%" (
    echo ✅ 桌面快捷方式创建成功！
) else (
    echo ⚠️  桌面快捷方式创建失败，但程序仍可运行
)

echo.
echo ========================================
echo 步骤7：创建开始菜单快捷方式
echo ========================================
echo.

echo 📋 正在创建开始菜单快捷方式...

set START_MENU_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\DesktopPet
if not exist "%START_MENU_DIR%" mkdir "%START_MENU_DIR%"

:: 创建开始菜单快捷方式
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP_DIR%\create_startmenu.vbs"
echo sLinkFile = "%START_MENU_DIR%\桌面宠物.lnk" >> "%TEMP_DIR%\create_startmenu.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP_DIR%\create_startmenu.vbs"
echo oLink.TargetPath = "%TARGET_PATH%" >> "%TEMP_DIR%\create_startmenu.vbs"
echo oLink.WorkingDirectory = "%INSTALL_DIR%" >> "%TEMP_DIR%\create_startmenu.vbs"
echo oLink.IconLocation = "%ICON_PATH%" >> "%TEMP_DIR%\create_startmenu.vbs"
echo oLink.Description = "桌面宠物程序" >> "%TEMP_DIR%\create_startmenu.vbs"
echo oLink.Save >> "%TEMP_DIR%\create_startmenu.vbs"

cscript //nologo "%TEMP_DIR%\create_startmenu.vbs"

if exist "%START_MENU_DIR%\桌面宠物.lnk" (
    echo ✅ 开始菜单快捷方式创建成功！
) else (
    echo ⚠️  开始菜单快捷方式创建失败
)

echo.
echo ========================================
echo 步骤8：完成安装
echo ========================================
echo.

echo 🎉 安装完成！
echo.
echo 📁 程序安装位置：%INSTALL_DIR%
echo 🖥️  桌面快捷方式：桌面宠物.lnk
echo 📋 开始菜单：开始菜单 > DesktopPet > 桌面宠物
echo.
echo 🚀 启动方式：
echo 1. 双击桌面上的"桌面宠物"图标
echo 2. 或进入安装目录，双击"run.bat"
echo.
echo 📖 使用说明：
echo - 首次运行需要选择一张照片生成宠物头像
echo - 右键点击宠物可以投喂食物
echo - 左键点击宠物可以触发动作
echo - 宠物会自动切换状态（站立→蹲下→睡眠）
echo.
echo ⚠️  注意事项：
echo 1. 如果遇到杀毒软件误报，请添加信任
echo 2. 程序需要网络连接下载依赖（仅首次）
echo 3. 退出程序时会自动保存状态
echo.
echo ========================================
echo 按任意键启动桌面宠物程序...
pause >nul

:: 启动程序
start "" "%INSTALL_DIR%\run.bat"

echo.
echo 程序已启动！宠物会出现在屏幕右下角
echo 按任意键退出安装程序...
pause >nul

goto :success_exit

:refresh_path
:: 刷新环境变量
for /f "skip=2 tokens=3*" %%a in ('reg query "HKCU\Environment" /v PATH 2^>nul') do set "USER_PATH=%%a %%b"
for /f "skip=2 tokens=3*" %%a in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PATH 2^>nul') do set "SYSTEM_PATH=%%a %%b"
set "PATH=%USER_PATH%;%SYSTEM_PATH%"
exit /b

:error_exit
echo.
echo ❌ 安装过程中出现错误
echo 请检查：
echo 1. 网络连接是否正常
echo 2. 是否有足够的磁盘空间
echo 3. 是否以管理员身份运行
echo.
echo 📞 获取帮助：
echo 访问项目页面：https://github.com/luomodeshang/desktop-pet
echo 查看用户指南：%INSTALL_DIR%\USER_GUIDE_小白版.md
echo.
pause
exit /b 1

:success_exit
echo.
echo ✅ 安装成功完成！
echo 感谢使用桌面宠物程序！
echo.
exit /b 0