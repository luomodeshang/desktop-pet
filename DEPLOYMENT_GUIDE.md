# 桌面宠物程序 - 完整部署指南

## 🎯 目标
让用户能够：**进入某个地址 → 下载安装包 → 运行EXE → 立即使用**

## 📁 文件结构总览
```
desktop_pet/
├── packaging/                    # 打包相关文件
│   ├── build_windows_exe.py     # 打包脚本
│   ├── pack_windows.bat         # Windows打包批处理
│   ├── setup_script.iss         # Inno Setup安装脚本
│   ├── download_page.html       # 下载页面
│   └── WINDOWS_PACKAGING_GUIDE.md
├── .github/workflows/           # GitHub Actions
│   └── build-windows.yml        # 自动构建工作流
├── USER_GUIDE_小白版.md         # 用户指南
├── README_Windows.md            # Windows使用说明
└── 原始项目文件...
```

## 🚀 快速部署方案

### 方案一：GitHub Releases（推荐）
**步骤：**
1. 在GitHub上创建Release
2. 上传打包好的EXE文件
3. 用户访问Releases页面下载

**优点：**
- 完全免费
- 版本管理方便
- 自动更新检查
- 下载统计

### 方案二：静态网站托管
**步骤：**
1. 使用GitHub Pages、Vercel、Netlify等
2. 部署 `download_page.html`
3. 配置下载链接

**优点：**
- 专业下载页面
- 更好的用户体验
- 可自定义域名

### 方案三：网盘分享
**步骤：**
1. 上传到百度网盘、Google Drive等
2. 分享下载链接
3. 设置提取码（可选）

**优点：**
- 国内访问速度快
- 无需服务器
- 简单直接

## 🔧 详细部署步骤

### 第一步：准备打包环境
```bash
# 在Windows电脑上操作
1. 安装 Python 3.8+ (64位)
2. 安装 Git
3. 克隆项目: git clone https://github.com/luomodeshang/desktop-pet.git
4. 进入项目目录: cd desktop-pet
```

### 第二步：运行打包脚本
```bash
# 方法A：使用批处理脚本（最简单）
双击 packaging/pack_windows.bat

# 方法B：手动打包
python packaging/build_windows_exe.py
```

### 第三步：创建安装包
```bash
# 使用 Inno Setup（推荐）
1. 下载安装 Inno Setup: https://jrsoftware.org/isdl.php
2. 打开 packaging/setup_script.iss
3. 编译生成 DesktopPet_Setup.exe
```

### 第四步：部署到下载地址

#### 选项A：GitHub Releases
```bash
1. 访问: https://github.com/luomodeshang/desktop-pet/releases
2. 点击 "Draft a new release"
3. 填写版本信息 (如: v1.0.0)
4. 上传文件:
   - DesktopPet_Setup.exe
   - DesktopPet_Windows_v1.0.0.zip
5. 发布
```

#### 选项B：静态网站
```bash
1. 复制 download_page.html 到网站根目录
2. 修改下载链接指向实际文件
3. 部署到:
   - GitHub Pages: https://pages.github.com/
   - Vercel: https://vercel.com/
   - Netlify: https://www.netlify.com/
```

#### 选项C：网盘分享
```bash
1. 登录网盘账户
2. 上传打包文件
3. 创建分享链接
4. 设置提取码（可选）
```

## 🌐 访问地址示例

### GitHub Releases
```
https://github.com/luomodeshang/desktop-pet/releases
```

### 自定义下载页面
```
https://luomodeshang.github.io/desktop-pet/
或
https://desktop-pet.vercel.app/
```

### 网盘链接
```
百度网盘: https://pan.baidu.com/s/xxxxxx
提取码: xxxx
```

## 📦 文件分发说明

### 1. 安装程序版 (DesktopPet_Setup.exe)
- **大小**: 约 50-100MB
- **包含**: 程序文件 + 安装向导
- **优点**: 专业安装体验，自动创建快捷方式
- **缺点**: 需要用户信任安装程序

### 2. 绿色免安装版 (DesktopPet_Windows_v1.0.0.zip)
- **大小**: 约 30-80MB
- **包含**: 解压即用
- **优点**: 无需安装，直接运行
- **缺点**: 需要用户手动解压

### 3. 源代码版
- **大小**: 约 5-10MB
- **包含**: Python源代码
- **优点**: 适合开发者
- **缺点**: 需要安装Python环境

## 🔄 自动更新机制

### GitHub Actions自动构建
每次推送标签时自动构建：
```yaml
git tag v1.0.1
git push origin v1.0.1
```

### 版本检查
程序启动时自动检查更新：
```python
# 在程序中添加版本检查
import requests
response = requests.get("https://api.github.com/repos/luomodeshang/desktop-pet/releases/latest")
latest_version = response.json()["tag_name"]
```

## 📊 用户统计（可选）

### 下载统计
1. **GitHub Releases**: 自带下载次数统计
2. **Google Analytics**: 添加到下载页面
3. **自定义统计**: 记录下载请求

### 使用统计
```python
# 在程序中添加匿名统计
import json
import requests

stats = {
    "version": "1.0.0",
    "action": "program_started",
    "timestamp": "2026-04-20T12:00:00"
}

# 发送到统计服务器（可选）
# requests.post("https://your-stats-server.com/track", json=stats)
```

## 🛡️ 安全考虑

### 代码签名（高级）
```bash
# 使用代码签名证书
signtool sign /f certificate.pfx /p password DesktopPet.exe
```

### 杀毒软件白名单
1. 提交到VirusTotal检查
2. 申请杀毒软件白名单
3. 提供MD5/SHA256校验码

### 用户数据安全
- 配置文件保存在用户目录
- 不收集个人信息
- 所有处理在本地完成

## 📱 多平台支持（未来扩展）

### Windows
- ✅ 已支持 (PyInstaller + Inno Setup)

### macOS
```bash
# 使用 py2app
pip install py2app
python setup.py py2app
```

### Linux
```bash
# 使用 AppImage
pip install pyinstaller
pyinstaller --onefile src/main.py
```

## 🆘 故障排除

### 常见问题
1. **程序无法启动**
   - 安装 VC++ Redistributable
   - 以管理员身份运行
   - 关闭杀毒软件

2. **下载链接失效**
   - 检查GitHub Releases
   - 更新下载页面链接
   - 提供备用下载地址

3. **安装失败**
   - 检查磁盘空间
   - 关闭其他程序
   - 重新下载安装包

### 用户支持
1. **GitHub Issues**: 技术问题
2. **Email**: 一般咨询
3. **文档**: 常见问题解答

## 🎯 最终用户流程
```
用户 → 访问下载页面 → 点击下载 → 运行安装包 → 选择照片 → 开始使用
      ↓           ↓           ↓           ↓           ↓
    GitHub      EXE文件     安装向导    照片处理    桌面宠物
    页面       或ZIP包      自动安装   动漫转换    互动程序
```

## 📝 检查清单
- [ ] 测试EXE文件在干净Windows系统上运行
- [ ] 验证所有功能正常工作
- [ ] 检查杀毒软件误报
- [ ] 更新下载页面链接
- [ ] 测试安装/卸载流程
- [ ] 准备用户支持渠道
- [ ] 创建版本说明文档
- [ ] 备份所有配置文件

## 🎉 完成！
现在用户可以通过简单的几步操作：
1. **访问**: GitHub Releases页面
2. **下载**: DesktopPet_Setup.exe
3. **安装**: 双击运行安装向导
4. **使用**: 选择照片，开始互动

**一句话总结：进入GitHub页面 → 下载安装包 → 双击运行 → 开始使用！**