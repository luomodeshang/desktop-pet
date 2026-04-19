#!/bin/bash
# 桌面宠物程序启动脚本

echo "启动桌面宠物程序..."

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python3"
    exit 1
fi

# 检查依赖
echo "检查Python依赖..."
pip3 install -r requirements.txt

# 启动程序
if [ "$1" == "--photo" ] && [ -n "$2" ]; then
    echo "使用照片: $2"
    python3 src/main.py "$2"
else
    echo "使用默认宠物形象"
    python3 src/main.py
fi