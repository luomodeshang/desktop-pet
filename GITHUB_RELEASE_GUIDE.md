# GitHub Release 创建指南

## 📋 准备工作

### 1. 确保所有文件已提交
```bash
git status  # 检查是否有未提交的更改
git add .   # 添加所有更改
git commit -m "准备发布 v1.0.1"
git push origin main
```

### 2. 创建版本标签（如果尚未创建）
```bash
# 查看现有标签
git tag

# 创建新标签
git tag -a v1.0.1 -m "桌面宠物程序 v1.0.1 发布版本"

# 推送标签到GitHub
git push origin v1.0.1
```

## 🚀 在GitHub网页上创建Release

### 步骤1：访问GitHub仓库
1. 打开浏览器，访问：https://github.com/luomodeshang/desktop-pet
2. 确保已登录GitHub账号

### 步骤2：进入Releases页面
1. 在仓库页面右侧，点击 **"Releases"** 链接
2. 或者直接访问：https://github.com/luomodeshang/desktop-pet/releases

### 步骤3：创建新Release
1. 点击 **"Create a new release"** 按钮
2. 或者点击 **"Draft a new release"**（如果有草稿）

### 步骤4：填写Release信息

#### 标签版本
- **Choose a tag**: 选择 `v1.0.1`（或输入 `v1.0.1` 创建新标签）
- **Target**: 选择 `main` 分支

#### Release标题
```
桌面宠物程序 v1.0.1
```

#### 描述内容
复制以下内容到描述框中：

```
# 桌面宠物程序 v1.0.1 发布说明

## 🎉 新版本发布！

**版本**: v1.0.1  
**发布日期**: 2026年4月23日  
**兼容性**: Windows 10/11, Python 3.8+

## 📦 下载链接

### 源代码包
- **desktop-pet-v1.0.1-source.tar.gz** - 完整源代码（适合开发者）
- 包含所有源代码、资源和打包脚本

### Windows用户包  
- **desktop-pet-v1.0.1-windows.tar.gz** - Windows用户专用包
- 包含运行所需的所有文件
- 需要安装Python 3.8+环境

## 🚀 快速开始

### 对于开发者/高级用户
1. 下载 **源代码包**
2. 解压：`tar -xzf desktop-pet-v1.0.1-source.tar.gz`
3. 安装依赖：`pip install -r requirements.txt`
4. 运行：`python src/main.py`

### 对于Windows普通用户
1. 下载 **Windows用户包**
2. 解压到任意目录
3. 确保已安装Python 3.8+
4. 双击 `run.bat` 或运行 `python src/main.py`

## 🎮 功能特色

### 🖼️ 照片转动漫
- 使用你的照片生成动漫风格宠物
- 智能人脸识别，保留原照片特征

### 🍔 投喂互动
- 右键点击投喂三种食物：汉堡、炸鸡、螺蛳粉
- 宠物有不同的吃食动画

### 👆 动作互动
- 左键点击触发三种动作：挥手、跳跃、踱步
- 宠物随机展示不同动作

### 💤 智能状态
- 自动切换状态：站立 → 蹲下 → 睡觉
- 长时间不动会自动睡觉
- 点击唤醒，恢复活力

### 💾 自动保存
- 退出时自动保存宠物状态
- 下次启动恢复位置和状态

## 🛠️ 技术改进

### v1.0.1 新增功能
- ✅ 完整的打包脚本支持
- ✅ Windows专用文档和指南
- ✅ GitHub Actions自动构建工作流
- ✅ 改进的用户体验和错误处理

## 📋 系统要求

| 组件 | 最低要求 | 推荐配置 |
|------|----------|----------|
| **操作系统** | Windows 10 | Windows 11 |
| **Python版本** | 3.8+ | 3.10+ |
| **内存** | 4 GB | 8 GB |
| **存储空间** | 200 MB | 500 MB |

## 🔧 安装说明

### 完整安装步骤
1. **安装Python 3.8+**
   - 访问 https://www.python.org/downloads/
   - 下载并安装Python（勾选"Add Python to PATH"）

2. **下载并解压程序**
   ```bash
   # 下载源代码包
   tar -xzf desktop-pet-v1.0.1-source.tar.gz
   cd desktop-pet
   
   # 或下载Windows用户包
   tar -xzf desktop-pet-v1.0.1-windows.tar.gz
   cd desktop-pet
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **运行程序**
   ```bash
   python src/main.py
   ```

## 🐛 常见问题

### 1. 程序无法启动
- 确保已安装 Microsoft Visual C++ Redistributable
- 尝试以管理员身份运行
- 检查杀毒软件是否误报

### 2. 照片处理失败
- 确保照片格式为 JPG/PNG
- 照片大小建议 500x500 像素以上
- 避免使用过大的照片

### 3. 依赖安装失败
- 使用国内镜像源：`pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`
- 确保网络连接正常
- 尝试更新pip：`pip install --upgrade pip`

## 📞 技术支持

### 问题反馈
- **GitHub Issues**: [提交问题](https://github.com/luomodeshang/desktop-pet/issues)
- **Email**: 1024656097@qq.com
- **文档**: 查看包内的README文件

### 反馈模板
```
问题描述：
操作步骤：
期望结果：
实际结果：
截图/日志：
系统信息：
```

## 🔄 更新日志

### v1.0.1 (2026-04-23)
- 新增完整的打包脚本和安装程序支持
- 添加详细的Windows用户文档
- 集成GitHub Actions自动构建
- 优化代码结构和错误处理

### v1.0.0 (2026-04-20)
- 初始版本发布
- 基本功能：照片转动漫、投喂互动、动作触发
- 状态自动保存和恢复

## 🙏 致谢

感谢所有测试用户和贡献者！

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

**开始你的桌面宠物之旅吧！** 🐾

*版本: v1.0.1 | 开发者: luomodeshang | 更新日期: 2026年4月23日*
```

#### 附件上传
1. 将 **desktop-pet-v1.0.1-source.tar.gz** 拖到附件区域
2. 将 **desktop-pet-v1.0.1-windows.tar.gz** 拖到附件区域

#### 发布设置
- **☑️ Set as latest release**（勾选此项，设为最新版本）
- **☑️ Create a discussion for this release**（可选，创建讨论）

### 步骤5：发布
1. 点击 **"Publish release"** 按钮
2. 等待发布完成

## 📊 发布后操作

### 1. 验证发布
1. 访问Release页面：https://github.com/luomodeshang/desktop-pet/releases
2. 确认v1.0.1版本显示为最新
3. 确认两个附件文件可以正常下载

### 2. 更新README
1. 编辑 `README.md` 文件
2. 添加下载链接：
   ```markdown
   ## 📥 下载
   
   最新版本: v1.0.1
   
   - [源代码包](https://github.com/luomodeshang/desktop-pet/releases/download/v1.0.1/desktop-pet-v1.0.1-source.tar.gz)
   - [Windows用户包](https://github.com/luomodeshang/desktop-pet/releases/download/v1.0.1/desktop-pet-v1.0.1-windows.tar.gz)
   
   查看所有版本: [Releases页面](https://github.com/luomodeshang/desktop-pet/releases)
   ```

### 3. 分享发布
1. 复制Release链接：https://github.com/luomodeshang/desktop-pet/releases/tag/v1.0.1
2. 分享给用户或社区

## 🔧 故障排除

### 问题1：无法上传附件
- 确保文件大小不超过2GB
- 检查网络连接
- 尝试使用其他浏览器

### 问题2：标签已存在
- 如果v1.0.1标签已存在，可以：
  1. 删除旧标签：`git tag -d v1.0.1` 和 `git push origin --delete v1.0.1`
  2. 创建新标签：`git tag -a v1.0.1 -m "新版本"`
  3. 或使用新版本号：v1.0.2

### 问题3：权限不足
- 确保你是仓库所有者或有写入权限
- 检查GitHub账号权限

## 💡 最佳实践

### 版本命名
- 使用语义化版本：`主版本.次版本.修订版本`
- 示例：v1.0.1, v1.1.0, v2.0.0

### 发布频率
- 重大功能更新：主版本（v1.0.0 → v2.0.0）
- 新功能添加：次版本（v1.0.0 → v1.1.0）
- Bug修复：修订版本（v1.0.0 → v1.0.1）

### 文档更新
- 每次发布都更新CHANGELOG.md
- 保持README.md中的下载链接最新
- 提供升级指南（如果有重大变更）

## 📞 帮助与支持

如果遇到问题：
1. 查看GitHub文档：https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases
2. 在仓库Issues中提问
3. 联系开发者：1024656097@qq.com

---
**祝发布顺利！** 🚀

*最后更新: 2026年4月23日*