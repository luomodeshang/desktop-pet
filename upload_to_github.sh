#!/bin/bash
# 一键上传到GitHub脚本

echo "桌面宠物项目上传到GitHub"
echo "=========================="

# 检查参数
if [ -z "$1" ]; then
    echo "用法: $0 <GitHub仓库URL>"
    echo "示例: $0 https://github.com/你的用户名/desktop-pet.git"
    echo "或: $0 git@github.com:你的用户名/desktop-pet.git"
    exit 1
fi

REPO_URL="$1"

echo "仓库URL: $REPO_URL"
echo ""

# 检查Git配置
echo "检查Git配置..."
USER_NAME=$(git config --global user.name)
USER_EMAIL=$(git config --global user.email)

if [ -z "$USER_NAME" ] || [ -z "$USER_EMAIL" ]; then
    echo "⚠️ Git用户信息未配置"
    read -p "请输入你的名字: " name
    read -p "请输入你的邮箱: " email
    git config --global user.name "$name"
    git config --global user.email "$email"
    echo "✓ Git用户信息已设置"
fi

echo "Git用户: $USER_NAME <$USER_EMAIL>"
echo ""

# 添加远程仓库
echo "添加远程仓库..."
git remote remove origin 2>/dev/null
git remote add origin "$REPO_URL"

if [ $? -ne 0 ]; then
    echo "✗ 添加远程仓库失败"
    exit 1
fi

echo "✓ 远程仓库添加成功"
echo ""

# 推送代码
echo "推送代码到GitHub..."
echo "这可能需要一些时间..."

# 尝试推送到main分支
if git push -u origin main 2>/dev/null; then
    echo "✓ 代码推送成功 (main分支)"
elif git push -u origin master 2>/dev/null; then
    echo "✓ 代码推送成功 (master分支)"
else
    echo "尝试重命名分支并推送..."
    git branch -M main 2>/dev/null
    git push -u origin main
fi

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 上传成功！"
    echo ""
    echo "下一步:"
    echo "1. 访问你的GitHub仓库页面"
    echo "2. 检查所有文件是否上传成功"
    echo "3. 分享仓库链接给其他人"
    echo ""
    echo "仓库URL:"
    echo "  https://github.com/$(echo "$REPO_URL" | sed 's|.*github.com/||' | sed 's|\.git$||')"
else
    echo "✗ 上传失败，请检查:"
    echo "  1. 仓库URL是否正确"
    echo "  2. 是否有写入权限"
    echo "  3. 网络连接是否正常"
fi
