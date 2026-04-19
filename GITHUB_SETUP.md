# GitHub上传指南

## 步骤1: 创建GitHub仓库

1. 登录 [GitHub](https://github.com)
2. 点击右上角 "+" → "New repository"
3. 填写仓库信息:
   - Repository name: `desktop-pet` (或你喜欢的名字)
   - Description: "一个可爱的桌面宠物程序"
   - 选择: Public (公开)
   - 不要初始化README（我们已经有了）
4. 点击 "Create repository"

## 步骤2: 配置本地Git

```bash
# 设置Git用户信息（如果还没设置）
git config --global user.name "你的名字"
git config --global user.email "你的邮箱@example.com"

# 查看当前配置
git config --global --list
```

## 步骤3: 连接到GitHub仓库

创建仓库后，GitHub会显示命令，类似：

```bash
# 添加远程仓库（替换YOUR_USERNAME为你的GitHub用户名）
git remote add origin https://github.com/YOUR_USERNAME/desktop-pet.git

# 或者使用SSH（推荐）
git remote add origin git@github.com:YOUR_USERNAME/desktop-pet.git
```

## 步骤4: 推送代码

```bash
# 推送到GitHub
git push -u origin main

# 如果遇到错误，可能需要重命名分支
git branch -M main
git push -u origin main
```

## 步骤5: 验证上传

1. 刷新GitHub仓库页面
2. 应该能看到所有文件
3. README.md会自动显示

## 步骤6: 添加标签和发布（可选）

```bash
# 创建版本标签
git tag v1.0.0
git push origin v1.0.0

# 在GitHub上创建Release
# 1. 进入仓库 → Releases → Create new release
# 2. 选择标签 v1.0.0
# 3. 填写发布说明
# 4. 上传可执行文件（如果需要）
```

## 常见问题

### 1. 权限错误
```bash
# 如果使用HTTPS遇到权限问题，改用SSH
git remote set-url origin git@github.com:YOUR_USERNAME/desktop-pet.git
```

### 2. 分支名称冲突
```bash
# 如果默认分支是master而不是main
git branch -M main
# 或者
git push -u origin master
```

### 3. 大文件上传
如果图片文件太大，可以考虑：
- 压缩图片
- 使用Git LFS
- 将大文件添加到.gitignore

## 后续维护

### 更新代码
```bash
# 修改代码后
git add .
git commit -m "更新说明"
git push
```

### 从GitHub拉取更新
```bash
git pull origin main
```

### 查看提交历史
```bash
git log --oneline --graph
```
