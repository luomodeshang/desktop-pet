@echo off
chcp 65001 >nul
echo.
echo ========================================
echo   桌面宠物程序 - Windows打包工具
echo ========================================
echo.

REM 检查Python是否安装
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ 未找到Python，请先安装Python 3.8+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 检查PyInstaller是否安装
python -c "import pyinstaller" 2>nul
if %errorlevel% neq 0 (
    echo ⚠️ PyInstaller未安装，正在安装...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        echo ❌ PyInstaller安装失败
        pause
        exit /b 1
    )
    echo ✅ PyInstaller安装成功
)

REM 检查项目结构
if not exist "src\main.py" (
    echo ❌ 未找到主程序文件 src\main.py
    echo 请确保在项目根目录运行此脚本
    pause
    exit /b 1
)

if not exist "config\settings.json" (
    echo ❌ 未找到配置文件 config\settings.json
    pause
    exit /b 1
)

echo.
echo 📦 开始打包桌面宠物程序...
echo.

REM 创建dist目录
if not exist "dist" mkdir dist

REM 清理旧的打包文件
if exist "build" rmdir /s /q build
if exist "dist\DesktopPet" rmdir /s /q dist\DesktopPet

REM 运行PyInstaller打包
echo 🚀 正在打包程序...
python -m PyInstaller --clean --noconfirm ^
    --name="DesktopPet" ^
    --onefile ^
    --windowed ^
    --icon="assets\images\icon.ico" ^
    --add-data="config;config" ^
    --add-data="assets;assets" ^
    --hidden-import="PyQt5" ^
    --hidden-import="PIL" ^
    --hidden-import="cv2" ^
    --hidden-import="numpy" ^
    src\main.py

if %errorlevel% neq 0 (
    echo ❌ 打包失败！
    pause
    exit /b 1
)

echo.
echo ✅ 打包完成！
echo.

REM 创建绿色版ZIP包
echo 📦 创建绿色免安装版...
if exist "dist\DesktopPet_Windows_v1.0.0.zip" del "dist\DesktopPet_Windows_v1.0.0.zip"

REM 创建临时目录结构
mkdir "dist\temp_package"
mkdir "dist\temp_package\DesktopPet"
copy "dist\DesktopPet.exe" "dist\temp_package\DesktopPet\DesktopPet.exe"
xcopy "config" "dist\temp_package\DesktopPet\config" /E /I /Y
xcopy "assets" "dist\temp_package\DesktopPet\assets" /E /I /Y

REM 创建说明文件
echo 桌面宠物程序 - 绿色免安装版 > "dist\temp_package\DesktopPet\README.txt"
echo ============================== >> "dist\temp_package\DesktopPet\README.txt"
echo. >> "dist\temp_package\DesktopPet\README.txt"
echo 使用方法： >> "dist\temp_package\DesktopPet\README.txt"
echo 1. 解压此ZIP包到任意目录 >> "dist\temp_package\DesktopPet\README.txt"
echo 2. 双击运行 DesktopPet.exe >> "dist\temp_package\DesktopPet\README.txt"
echo 3. 首次运行选择一张照片 >> "dist\temp_package\DesktopPet\README.txt"
echo 4. 开始与桌面宠物互动！ >> "dist\temp_package\DesktopPet\README.txt"
echo. >> "dist\temp_package\DesktopPet\README.txt"
echo 功能说明： >> "dist\temp_package\DesktopPet\README.txt"
echo - 左键点击：触发动作（挥手、跳跃、踱步） >> "dist\temp_package\DesktopPet\README.txt"
echo - 右键点击：投喂食物（汉堡、炸鸡、螺蛳粉） >> "dist\temp_package\DesktopPet\README.txt"
echo - 拖动宠物：移动位置 >> "dist\temp_package\DesktopPet\README.txt"
echo - 长时间不动：自动切换状态（站立→蹲下→睡觉） >> "dist\temp_package\DesktopPet\README.txt"
echo. >> "dist\temp_package\DesktopPet\README.txt"
echo 项目地址：https://github.com/luomodeshang/desktop-pet >> "dist\temp_package\DesktopPet\README.txt"

REM 创建ZIP包
cd "dist\temp_package"
powershell -Command "Compress-Archive -Path 'DesktopPet' -DestinationPath '..\DesktopPet_Windows_v1.0.0.zip' -Force"
cd ..\..

if exist "dist\DesktopPet_Windows_v1.0.0.zip" (
    echo ✅ 绿色版创建成功: dist\DesktopPet_Windows_v1.0.0.zip
) else (
    echo ⚠️ 绿色版创建失败，但EXE文件已生成
)

REM 清理临时文件
if exist "dist\temp_package" rmdir /s /q "dist\temp_package"

echo.
echo 📊 打包结果：
echo.
dir dist\DesktopPet.exe
if exist "dist\DesktopPet_Windows_v1.0.0.zip" (
    echo.
    dir dist\DesktopPet_Windows_v1.0.0.zip
)

echo.
echo 🎉 打包完成！文件已生成在 dist\ 目录：
echo.
echo 1. 单文件EXE: dist\DesktopPet.exe
echo 2. 绿色版ZIP: dist\DesktopPet_Windows_v1.0.0.zip
echo.
echo 📝 下一步：
echo 1. 测试 EXE 文件是否正常工作
echo 2. 上传到 GitHub Releases
echo 3. 分享给用户下载使用
echo.
echo 按任意键退出...
pause >nul