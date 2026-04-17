@echo off
REM Windows启动脚本

echo 启动桌面宠物程序...

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python3
    pause
    exit /b 1
)

REM 安装依赖
echo 安装Python依赖...
pip install -r requirements.txt

REM 启动程序
if "%1"=="--photo" (
    if not "%2"=="" (
        echo 使用照片: %2
        python src/main.py "%2"
    ) else (
        echo 错误: 请提供照片路径
        pause
    )
) else (
    echo 使用默认宠物形象
    python src/main.py
)

pause