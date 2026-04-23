@echo off
chcp 65001 >nul
title 桌面宠物程序 - 环境检查工具
color 0B

echo ========================================
echo     桌面宠物程序环境检查工具
echo ========================================
echo.
echo 此工具检查您的电脑是否满足运行要求
echo 并提供具体的解决建议
echo.
echo 按任意键开始检查...
pause >nul

echo.
echo ========================================
echo 第1步：检查操作系统
echo ========================================
echo.

ver | find "Windows" >nul
if %errorLevel% equ 0 (
    ver
    echo ✅ 检测到Windows系统
) else (
    echo ❌ 未检测到Windows系统
    echo 此程序仅支持Windows系统
    goto :end_check
)

echo.
echo ========================================
echo 第2步：检查系统架构
echo ========================================
echo.

echo %PROCESSOR_ARCHITECTURE% | find "64" >nul
if %errorLevel% equ 0 (
    echo ✅ 64位系统（推荐）
) else (
    echo ⚠️  检测到32位系统
    echo 程序可能需要特殊版本
)

echo.
echo ========================================
echo 第3步：检查Python环境
echo ========================================
echo.

where python >nul 2>&1
if %errorLevel% equ 0 (
    python --version
    echo ✅ Python已安装
    
    :: 检查Python版本
    python -c "import sys; print('Python版本:', sys.version.split()[0])" 2>nul
    echo ✅ Python版本检查完成
) else (
    echo ❌ Python未安装
    echo 需要安装Python 3.7或更高版本
    set PYTHON_MISSING=1
)

echo.
echo ========================================
echo 第4步：检查pip工具
echo ========================================
echo.

where pip >nul 2>&1
if %errorLevel% equ 0 (
    pip --version
    echo ✅ pip已安装
) else (
    echo ❌ pip未安装
    echo 需要pip来安装Python库
    set PIP_MISSING=1
)

echo.
echo ========================================
echo 第5步：检查磁盘空间
echo ========================================
echo.

for /f "tokens=3" %%a in ('dir /-c %SystemDrive% ^| find "可用字节"') do set FREE_SPACE=%%a
set /a FREE_SPACE_MB=FREE_SPACE/1048576

if %FREE_SPACE_MB% GTR 500 (
    echo ✅ 磁盘空间充足：%FREE_SPACE_MB% MB
) else if %FREE_SPACE_MB% GTR 200 (
    echo ⚠️  磁盘空间较低：%FREE_SPACE_MB% MB
    echo 建议清理至少500MB空间
) else (
    echo ❌ 磁盘空间不足：%FREE_SPACE_MB% MB
    echo 需要至少200MB可用空间
    set SPACE_INSUFFICIENT=1
)

echo.
echo ========================================
echo 第6步：检查网络连接
echo ========================================
echo.

ping -n 1 github.com >nul 2>&1
if %errorLevel% equ 0 (
    echo ✅ 网络连接正常
) else (
    echo ❌ 无法连接到GitHub
    echo 安装需要网络连接下载文件
    set NETWORK_ISSUE=1
)

echo.
echo ========================================
echo 检查结果汇总
echo ========================================
echo.

if defined PYTHON_MISSING (
    echo ❌ 主要问题：Python未安装
    echo   解决方案：运行Windows一键获取器自动安装
) else if defined PIP_MISSING (
    echo ⚠️  次要问题：pip未安装
    echo   解决方案：Python安装时自动包含
) else (
    echo ✅ 环境检查通过！
    echo   可以正常运行桌面宠物程序
)

echo.
if defined SPACE_INSUFFICIENT (
    echo ⚠️  警告：磁盘空间不足
    echo   建议清理磁盘空间
)

if defined NETWORK_ISSUE (
    echo ⚠️  警告：网络连接问题
    echo   需要网络连接下载程序文件
)

echo.
echo ========================================
echo 推荐操作
echo ========================================
echo.

if defined PYTHON_MISSING (
    echo 🚀 推荐使用：Windows一键获取器.bat
    echo   自动安装Python和所有依赖
) else if defined PIP_MISSING (
    echo 🚀 推荐使用：Windows小白专用安装器.bat
    echo   自动安装缺失组件
) else (
    echo 🚀 推荐使用：Windows一键获取器.bat
    echo   快速获取并安装程序
)

echo.
echo 📋 可用安装选项：
echo 1. Windows一键获取器.bat - 最简单的获取方式
echo 2. Windows小白专用安装器.bat - 自动化安装
echo 3. Windows完整安装助手.bat - 完整功能安装
echo 4. Windows用户助手.bat - 智能环境检测

echo.
echo ========================================
echo 详细建议
echo ========================================
echo.

echo 根据您的检查结果：
echo.

if defined PYTHON_MISSING (
    echo 1. 您需要安装Python
    echo    下载Python 3.10：https://www.python.org/downloads/
    echo    安装时务必勾选"Add Python to PATH"
    echo.
)

if defined PIP_MISSING (
    echo 2. 您需要安装pip工具
    echo    运行：python -m ensurepip --upgrade
    echo.
)

if defined SPACE_INSUFFICIENT (
    echo 3. 您需要清理磁盘空间
    echo    删除临时文件和不必要的程序
    echo    目标：至少500MB可用空间
    echo.
)

if defined NETWORK_ISSUE (
    echo 4. 您需要解决网络问题
    echo    检查网络连接和防火墙设置
    echo    或使用离线安装包
    echo.
)

echo 5. 运行推荐的安装脚本
echo    按照屏幕提示完成安装
echo.

:end_check
echo ========================================
echo 按 1 运行Windows一键获取器，按 2 退出
choice /c 12 /n /m "请选择:"

if errorlevel 2 (
    echo.
    echo 感谢使用环境检查工具！
    echo 如需帮助，请查看WINDOWS_小白完全指南.md
) else if errorlevel 1 (
    echo.
    echo 🚀 启动Windows一键获取器...
    if exist "Windows_一键获取器.bat" (
        start "" "Windows_一键获取器.bat"
    ) else (
        echo ❌ 未找到Windows一键获取器.bat
        echo 请从GitHub下载：https://github.com/luomodeshang/desktop-pet
    )
)

echo.
pause
exit /b 0