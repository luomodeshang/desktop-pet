#!/bin/bash
echo "🔍 检查GitHub仓库状态..."
echo "================================"

# 检查远程仓库
echo "📦 远程仓库:"
git remote -v

echo ""
echo "📊 分支状态:"
git status

echo ""
echo "📝 最近提交:"
git log --oneline -3

echo ""
echo "🌐 检查GitHub连接..."
if curl -s https://api.github.com/repos/luomodeshang/desktop-pet | grep -q "Not Found"; then
    echo "❌ GitHub仓库不存在或无法访问"
else
    echo "✅ GitHub仓库可访问"
fi

echo ""
echo "📁 项目文件统计:"
echo "总文件数: $(find . -type f -not -path './.git/*' -not -path './venv/*' | wc -l)"
echo "Python文件: $(find . -name "*.py" -not -path './venv/*' | wc -l)"
echo "资源文件: $(find ./assets -type f 2>/dev/null | wc -l)"
echo "配置文件: $(find ./config -type f 2>/dev/null | wc -l)"

echo ""
echo "✅ GitHub提交完成！"
echo "仓库地址: https://github.com/luomodeshang/desktop-pet"