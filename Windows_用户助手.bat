@echo off
chcp 65001 >nul
REM ============================================
REM 桌面宠物程序 - 极简Windows版
REM 无需Python环境，直接运行
REM ============================================

echo.
echo ╔══════════════════════════════════════════╗
echo ║        桌面宠物程序 - Windows版          ║
echo ╚══════════════════════════════════════════╝
echo.

:check_requirements
echo 📋 检查系统要求...
echo.

REM 检查操作系统
ver | find "Windows" >nul
if %errorlevel% neq 0 (
    echo ❌ 此程序仅支持Windows系统
    pause
    exit /b 1
)

echo ✅ 操作系统: Windows
echo.

:check_github
echo 🔍 检查GitHub Releases...
echo.

echo 正在查找可用的EXE版本...
echo.

echo 📥 下载选项：
echo   1. 从GitHub Releases下载EXE文件（推荐）
echo   2. 使用Python运行源码（需要Python环境）
echo   3. 退出
echo.

set /p choice="请选择 (1-3): "

if "%choice%"=="1" goto download_exe
if "%choice%"=="2" goto run_with_python
if "%choice%"=="3" goto exit
echo 无效选择
goto check_github

:download_exe
echo.
echo ============================================
echo     从GitHub下载EXE文件
echo ============================================
echo.

echo 正在获取最新版本信息...
powershell -Command "
try {
    \$release = Invoke-RestMethod -Uri 'https://api.github.com/repos/luomodeshang/desktop-pet/releases/latest' -TimeoutSec 10
    echo '最新版本: ' + \$release.tag_name
    echo '发布时间: ' + \$release.published_at
    echo ''
    echo '可用文件:'
    foreach (\$asset in \$release.assets) {
        echo '  - ' + \$asset.name + ' (' + [math]::Round(\$asset.size/1MB, 2) + ' MB)'
    }
} catch {
    echo '❌ 无法获取版本信息'
    echo '可能原因:'
    echo '  1. 网络连接问题'
    echo '  2. 还没有发布EXE版本'
    echo '  3. GitHub API限制'
}
"

echo.
set /p confirm="是否下载EXE文件？(Y/N): "
if /i "%confirm%" neq "Y" goto check_github

echo.
echo 正在下载DesktopPet.exe...
powershell -Command "
try {
    \$url = 'https://github.com/luomodeshang/desktop-pet/releases/latest/download/DesktopPet.exe'
    echo '下载地址: ' + \$url
    Invoke-WebRequest -Uri \$url -OutFile 'DesktopPet.exe' -TimeoutSec 30
    if (Test-Path 'DesktopPet.exe') {
        \$size = (Get-Item 'DesktopPet.exe').Length / 1MB
        echo '✅ 下载完成: DesktopPet.exe (' + [math]::Round(\$size, 2) + ' MB)'
    } else {
        echo '❌ 下载失败'
    }
} catch {
    echo '❌ 下载失败: ' + \$_.Exception.Message
}
"

if exist DesktopPet.exe (
    echo.
    echo 🎉 EXE文件下载成功！
    echo.
    echo ⚠️  重要提示：
    echo   1. 首次运行时，杀毒软件可能报警
    echo   2. 请点击"更多信息" -> "仍要运行"
    echo   3. 程序完全安全，代码开源可查
    echo.
    echo 🖱️ 使用方法：
    echo   1. 双击 DesktopPet.exe
    echo   2. 选择一张照片生成宠物
    echo   3. 左键点击：触发动作
    echo   4. 右键点击：投喂食物
    echo   5. 拖动宠物：移动位置
    echo.
    set /p run="是否立即运行程序？(Y/N): "
    if /i "%run%"=="Y" (
        echo 正在启动桌面宠物程序...
        start DesktopPet.exe
    )
) else (
    echo.
    echo ⚠️  EXE文件尚未发布
    echo.
    echo 当前解决方案：
    echo   1. 等待GitHub Actions构建完成
    echo   2. 或使用Python运行源码版
    echo.
    set /p fallback="是否使用Python运行源码？(Y/N): "
    if /i "%fallback%"=="Y" goto run_with_python
)

goto exit

:run_with_python
echo.
echo ============================================
echo     使用Python运行源码版
echo ============================================
echo.

REM 检查Python
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ 检测到Python
    python --version
    goto check_python_deps
)

echo ❌ 未检测到Python
echo.
echo 安装Python步骤：
echo   1. 访问 https://www.python.org/downloads/
echo   2. 下载Python 3.10+ 安装包
echo   3. 安装时勾选"Add Python to PATH"
echo   4. 重新运行此脚本
echo.
pause
goto exit

:check_python_deps
echo.
echo 🔧 检查Python依赖...
echo.

REM 检查并安装依赖
echo 正在安装所需依赖...
pip install --upgrade pip

REM 临时requirements文件
echo Pillow^>=10.0.0 > temp_req.txt
echo opencv-python^>=4.8.0 >> temp_req.txt
echo numpy^>=1.24.0 >> temp_req.txt
echo PyQt5^>=5.15.0 >> temp_req.txt
echo PyQt5-sip^>=12.13.0 >> temp_req.txt

pip install -r temp_req.txt
del temp_req.txt

if %errorlevel% equ 0 (
    echo ✅ 依赖安装完成
) else (
    echo ❌ 依赖安装失败
    echo 请手动安装：pip install Pillow opencv-python numpy PyQt5
    pause
    goto exit
)

:run_program
echo.
echo 🚀 启动桌面宠物程序...
echo.

if exist src\main.py (
    echo 程序启动中...
    echo.
    echo 使用说明：
    echo   - 首次运行需选择照片
    echo   - 左键点击宠物：触发动作
    echo   - 右键点击宠物：投喂食物
    echo   - 拖动宠物：移动位置
    echo   - 自动保存状态
    echo.
    echo 按Ctrl+C可退出程序
    echo.
    pause
    python src\main.py
) else (
    echo ❌ 找不到主程序文件
    echo 请从GitHub下载完整源码：
    echo https://github.com/luomodeshang/desktop-pet
    pause
)

goto exit

:exit
echo.
echo ============================================
echo           程序信息
echo ============================================
echo.
echo 项目地址：https://github.com/luomodeshang/desktop-pet
echo 问题反馈：1024656097@qq.com
echo.
echo 按任意键退出...
pause >nul