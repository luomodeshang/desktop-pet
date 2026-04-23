@echo off
REM ============================================
REM 桌面宠物程序 - Windows一键安装脚本
REM 为没有Python环境的用户准备
REM ============================================

echo.
echo ============================================
echo     桌面宠物程序 Windows安装助手
echo ============================================
echo.

:menu
echo 请选择安装方式：
echo.
echo [1] 自动安装Python和所有依赖（推荐）
echo [2] 我已安装Python，只安装程序依赖
echo [3] 查看系统要求
echo [4] 退出
echo.
set /p choice="请选择 (1-4): "

if "%choice%"=="1" goto install_all
if "%choice%"=="2" goto install_deps_only
if "%choice%"=="3" goto system_requirements
if "%choice%"=="4" goto exit
echo 无效选择，请重新输入
goto menu

:install_all
echo.
echo ============================================
echo     步骤1：下载并安装Python 3.10
echo ============================================
echo.

REM 检查是否已安装Python
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ 检测到已安装Python
    python --version
    goto install_deps
)

echo 正在下载Python 3.10.11安装包...
powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe' -OutFile 'python_installer.exe'"

if exist python_installer.exe (
    echo.
    echo 请按照安装向导完成Python安装：
    echo 1. 勾选"Add Python 3.10 to PATH"
    echo 2. 点击"Install Now"
    echo 3. 等待安装完成
    echo.
    echo 安装完成后按任意键继续...
    pause >nul
    start /wait python_installer.exe
    del python_installer.exe
) else (
    echo ❌ Python安装包下载失败
    echo 请手动下载：https://www.python.org/downloads/
    pause
    goto exit
)

:install_deps
echo.
echo ============================================
echo     步骤2：安装程序依赖
echo ============================================
echo.

echo 正在安装桌面宠物程序依赖...
pip install --upgrade pip

REM 创建requirements.txt文件
echo # 桌面宠物程序依赖> requirements.txt
echo.>> requirements.txt
echo # 图像处理>> requirements.txt
echo Pillow^>=10.0.0>> requirements.txt
echo opencv-python^>=4.8.0>> requirements.txt
echo numpy^>=1.24.0>> requirements.txt
echo.>> requirements.txt
echo # GUI界面>> requirements.txt
echo PyQt5^>=5.15.0>> requirements.txt
echo PyQt5-sip^>=12.13.0>> requirements.txt

pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo ✅ 依赖安装完成
) else (
    echo ❌ 依赖安装失败
    pause
    goto exit
)

:download_program
echo.
echo ============================================
echo     步骤3：下载桌面宠物程序
echo ============================================
echo.

set /p download="是否下载最新版程序？(Y/N): "
if /i "%download%" neq "Y" goto run_program

echo 正在从GitHub下载最新版本...
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/luomodeshang/desktop-pet/archive/refs/heads/main.zip' -OutFile 'desktop-pet-latest.zip'"

if exist desktop-pet-latest.zip (
    echo 解压程序文件...
    powershell -Command "Expand-Archive -Path 'desktop-pet-latest.zip' -DestinationPath '.' -Force"
    move desktop-pet-main\* .
    rmdir /s /q desktop-pet-main
    del desktop-pet-latest.zip
    echo ✅ 程序下载完成
) else (
    echo ⚠️ 下载失败，使用本地文件（如果有）
)

:run_program
echo.
echo ============================================
echo     步骤4：运行桌面宠物程序
echo ============================================
echo.

if exist src\main.py (
    echo 正在启动桌面宠物程序...
    echo.
    echo 首次运行说明：
    echo 1. 程序会要求选择一张照片
    echo 2. 选择照片后生成动漫风格宠物
    echo 3. 左键点击：触发动作
    echo 4. 右键点击：投喂食物
    echo 5. 拖动宠物：移动位置
    echo.
    echo 按任意键启动程序...
    pause >nul
    python src\main.py
) else (
    echo ❌ 找不到主程序文件
    echo 请确保程序文件已下载
    pause
)

goto exit

:install_deps_only
echo.
echo 正在检查Python安装...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未检测到Python，请先安装Python
    pause
    goto menu
)
python --version
goto install_deps

:system_requirements
echo.
echo ============================================
echo           系统要求
echo ============================================
echo.
echo 最低配置：
echo - Windows 7/8/10/11 (64位)
echo - 4GB RAM
echo - 2GB可用磁盘空间
echo - 网络连接（用于下载）
echo.
echo 推荐配置：
echo - Windows 10/11 (64位)
echo - 8GB RAM
echo - 支持OpenGL的显卡
echo.
echo 按任意键返回菜单...
pause >nul
goto menu

:exit
echo.
echo ============================================
echo     安装助手已完成
echo ============================================
echo.
echo 如需再次运行，请双击此批处理文件
echo.
echo 技术支持：
echo - GitHub: https://github.com/luomodeshang/desktop-pet
echo - 邮箱: 1024656097@qq.com
echo.
pause