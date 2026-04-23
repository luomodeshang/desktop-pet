# 桌面宠物程序

## 🎯 目标用户
- **Windows小白用户**：没有Python环境，不懂编程
- **普通用户**：想要简单双击就能用的程序
- **开发者**：想要源代码和自定义功能

## 📥 下载（针对不同用户类型）

### 🪟 对于Windows小白用户（最简单！）
**你没有任何技术基础？没问题！**

**推荐方案**：
1. 下载 [Windows_一键获取器.bat](Windows_一键获取器.bat)
2. 双击运行
3. 按照提示操作
4. 完成！桌面会出现"桌面宠物"图标

**其他选项**（任选其一）：
- [Windows_小白专用安装器.bat](Windows_小白专用安装器.bat) - 专为小白设计
- [Windows_完整安装助手.bat](Windows_完整安装助手.bat) - 完整功能安装
- [Windows_用户助手.bat](Windows_用户助手.bat) - 智能环境检测
- [Windows_一键安装助手.bat](Windows_一键安装助手.bat) - 快速安装

**先检查环境**：
- [Windows_环境检查工具.bat](Windows_环境检查工具.bat) - 检查电脑是否满足要求

### 💻 对于普通用户（已有Python环境）
如果你已经安装了Python：
1. 下载 [源代码包](https://github.com/luomodeshang/desktop-pet/releases/download/v1.0.2/desktop-pet-v1.0.2-source.tar.gz)
2. 解压文件
3. 安装依赖：`pip install -r requirements.txt`
4. 运行：`python src/main.py`

### 🛠️ 对于开发者
1. 克隆仓库：`git clone https://github.com/luomodeshang/desktop-pet.git`
2. 创建虚拟环境：`python -m venv venv`
3. 激活环境：`source venv/bin/activate` (Linux/Mac) 或 `venv\Scripts\activate` (Windows)
4. 安装依赖：`pip install -r requirements.txt`
5. 运行：`python src/main.py`

## 📚 用户指南

### 小白用户必读
- [WINDOWS_小白完全指南.md](WINDOWS_小白完全指南.md) - 从零开始的完全指南
- [WINDOWS_终极解决方案_v2.md](WINDOWS_终极解决方案_v2.md) - 所有解决方案汇总
- [USER_GUIDE_小白版.md](USER_GUIDE_小白版.md) - 基础使用指南

### 技术文档
- [WINDOWS_USER_GUIDE_EXE.md](WINDOWS_USER_GUIDE_EXE.md) - EXE文件使用指南
- [README_Windows.md](README_Windows.md) - Windows专用指南
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - 部署指南

## 🎯 功能特性
- 🖼️ 使用你的照片生成动漫风格宠物
- 🍔 右键投喂（汉堡、炸鸡、螺蛳粉）
- 👋 左键点击触发动作（挥手、跳跃、踱步）
- 😴 闲置时自动切换状态（站立→蹲下→睡眠）
- 💾 状态自动保存
- 🎨 支持自定义宠物外观
- ⚙️ 可配置的行为参数

## 🚀 快速开始（小白用户版）

### 第一步：获取程序
1. 点击 [Windows_一键获取器.bat](Windows_一键获取器.bat) 下载
2. 如果浏览器阻止下载，选择"保留"或"允许"

### 第二步：运行安装
1. 找到下载的 `Windows_一键获取器.bat` 文件
2. 双击运行
3. 如果出现安全警告，点击"更多信息" → "仍要运行"
4. 按照屏幕提示操作

### 第三步：使用程序
1. 安装完成后，桌面上会出现"桌面宠物"图标
2. 双击图标启动程序
3. 首次运行选择一张照片
4. 开始享受你的桌面宠物！

## 🐾 基本操作
- **选择照片**：首次运行选择一张照片，程序会自动生成动漫风格宠物
- **右键点击**：投喂食物（汉堡🍔、炸鸡🍗、螺蛳粉🍜）
- **左键点击**：触发动作（挥手👋、跳跃🤸、踱步🚶）
- **自动活动**：宠物会自己切换状态（站立→蹲下→睡眠）
- **拖动移动**：用鼠标拖动宠物到喜欢的位置
- **系统托盘**：右键托盘图标可以退出程序

## ⚠️ 常见问题

### 问题1：杀毒软件误报
```
解决方法：
1. 打开杀毒软件
2. 找到"信任列表"或"排除列表"
3. 添加桌面宠物程序文件夹
4. 或暂时关闭杀毒软件安装
```

### 问题2：Python安装失败
```
解决方法：
1. 手动下载Python：https://www.python.org/downloads/
2. 下载Python 3.10版本
3. 安装时务必勾选"Add Python to PATH"
4. 重新运行安装器
```

### 问题3：程序无法启动
```
解决方法：
1. 运行 Windows_环境检查工具.bat
2. 按照检查结果解决问题
3. 或尝试其他安装脚本
```

## 🔧 文件结构
```
桌面宠物程序/
├── Windows_一键获取器.bat        # 最简单的获取方式（推荐！）
├── Windows_小白专用安装器.bat     # 小白用户专用
├── Windows_完整安装助手.bat       # 完整功能安装
├── Windows_用户助手.bat          # 智能环境检测
├── Windows_一键安装助手.bat      # 快速安装
├── Windows_环境检查工具.bat      # 环境检查
├── src/                         # 程序源代码
├── assets/                      # 资源文件
│   └── images/                  # 图片和图标
├── config/                      # 配置文件
├── run.bat                      # 启动脚本
└── 各种用户指南.md               # 使用说明文档
```

## 📞 获取帮助

### 在线资源
- **GitHub项目页**：https://github.com/luomodeshang/desktop-pet
- **问题反馈**：GitHub Issues
- **社区讨论**：GitHub Discussions

### 本地帮助
1. 查看安装目录中的用户指南
2. 运行程序内的帮助功能
3. 查看错误日志文件

## 🔄 更新程序
程序会自动检查更新。当有新版本时：
1. 程序会提示更新
2. 点击"立即更新"
3. 等待下载完成
4. 重新启动程序

## 🎨 自定义设置
- **修改宠物外观**：准备新照片，重新运行程序选择
- **添加自定义食物**：编辑 `config/config.json` 文件
- **调整宠物行为**：修改配置文件中的参数

---

**最后更新**：2026年4月23日  
**当前版本**：v1.0.7  
**适用系统**：Windows 7/8/10/11  

> 💡 **提示**：如果遇到任何问题，请先运行 `Windows_环境检查工具.bat`，然后查看对应的用户指南文档。