#!/bin/bash
echo "=== GitHub上传验证 ==="
echo ""

echo "1. 本地仓库状态:"
git status --short

echo ""
echo "2. 远程仓库:"
git remote -v

echo ""
echo "3. 提交历史:"
git log --oneline -5

echo ""
echo "4. 测试拉取:"
git fetch --dry-run

echo ""
echo "5. GitHub仓库地址:"
echo "   https://github.com/luomodeshang/desktop-pet"
echo ""
echo "6. 请访问上面的链接确认:"
echo "   - 所有文件是否都在"
echo "   - README.md是否正常显示"
echo "   - 提交历史是否正确"
echo ""
echo "验证完成！"
