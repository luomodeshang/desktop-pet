#!/usr/bin/env python3
"""
Windows EXE打包脚本
在Windows电脑上运行此脚本来创建桌面宠物的可执行文件
"""

import os
import sys
import shutil
import subprocess
import json
from pathlib import Path

def check_pyinstaller():
    """检查PyInstaller是否已安装"""
    try:
        import PyInstaller
        print("✅ PyInstaller 已安装")
        return True
    except ImportError:
        print("❌ PyInstaller 未安装，正在安装...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✅ PyInstaller 安装成功")
            return True
        except Exception as e:
            print(f"❌ 安装PyInstaller失败: {e}")
            return False

def create_spec_file():
    """创建PyInstaller spec文件"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets/images/', 'assets/images/'),
        ('config/', 'config/'),
        ('requirements.txt', '.'),
        ('README.md', '.'),
    ],
    hiddenimports=[
        'PyQt5',
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'cv2',
        'PIL',
        'numpy',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='DesktopPet',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 不显示控制台窗口
    icon='assets/images/cartoon_pet.ico' if os.path.exists('assets/images/cartoon_pet.ico') else None,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='DesktopPet',
)
'''
    
    with open('desktop_pet.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    print("✅ 已创建 spec 文件")

def create_installer_script():
    """创建安装脚本"""
    installer_content = '''@echo off
chcp 65001 >nul
echo ========================================
echo       桌面宠物程序安装向导
echo ========================================
echo.

REM 检查Python是否已安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未检测到Python，请先安装Python 3.8+
    echo 访问 https://www.python.org/downloads/ 下载安装
    pause
    exit /b 1
)

echo ✅ 检测到Python已安装

REM 检查虚拟环境
if not exist "venv" (
    echo 正在创建虚拟环境...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ 创建虚拟环境失败
        pause
        exit /b 1
    )
    echo ✅ 虚拟环境创建成功
)

REM 激活虚拟环境并安装依赖
echo 正在安装依赖...
call venv\\Scripts\\activate.bat
pip install --upgrade pip
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ 依赖安装失败
    pause
    exit /b 1
)

echo ✅ 依赖安装成功
echo.
echo ========================================
echo       安装完成！
echo ========================================
echo.
echo 运行方法：
echo 1. 双击 run.bat 启动程序
echo 2. 或者运行：python src/main.py
echo.
echo 注意事项：
echo - 首次运行需要选择一张照片生成宠物头像
echo - 右键点击宠物可以投喂食物
echo - 左键点击宠物触发动作
echo - 拖动宠物可以移动位置
echo.
pause
'''
    
    with open('install.bat', 'w', encoding='utf-8') as f:
        f.write(installer_content)
    print("✅ 已创建安装脚本")

def create_readme_for_windows():
    """创建Windows用户使用说明"""
    readme_content = '''# 桌面宠物程序 - Windows版

## 🎯 功能特点
- 🖼️ 使用你的照片生成动漫风格宠物
- 🍔 右键投喂（汉堡、炸鸡、螺蛳粉）
- 👆 左键点击触发动作（挥手、跳跃、踱步）
- 😴 闲置时自动切换状态（站立→蹲下→睡眠）
- 💾 状态自动保存

## 🚀 快速开始

### 方法一：使用安装包（推荐）
1. 下载 `DesktopPet_Setup.exe`
2. 双击运行安装程序
3. 按照向导完成安装
4. 桌面或开始菜单中找到"桌面宠物"并运行

### 方法二：手动安装
1. 下载项目文件
2. 双击 `install.bat` 运行安装脚本
3. 安装完成后双击 `run.bat` 启动程序

## 🎮 使用方法

### 基本操作
- **左键点击宠物**：触发动作（挥手、跳跃、踱步）
- **右键点击宠物**：显示投喂菜单
- **拖动宠物**：移动宠物位置
- **系统托盘图标**：右键退出程序

### 首次运行
1. 程序启动后会提示选择一张照片
2. 选择你的照片后，程序会自动生成动漫风格宠物
3. 宠物会显示在桌面右下角

## ⚙️ 配置说明

### 配置文件位置
- `config/settings.json` - 程序设置
- `config/image_paths.json` - 图像路径

### 自定义设置
你可以修改 `config/settings.json` 文件来自定义：
- 宠物大小
- 动画速度
- 闲置时间
- 食物列表
- 动作列表

## 🛠️ 常见问题

### 1. 程序无法启动
- 确保已安装 Microsoft Visual C++ Redistributable
- 尝试以管理员身份运行
- 检查杀毒软件是否误报

### 2. 照片处理失败
- 确保照片格式为 JPG/PNG
- 照片大小建议 500x500 像素以上
- 避免使用过大的照片

### 3. 宠物显示异常
- 检查 `assets/images/` 目录是否存在
- 确保图像文件完整
- 重启程序

## 📁 文件结构
```
DesktopPet/
├── DesktopPet.exe          # 主程序
├── assets/images/          # 图像资源
├── config/                 # 配置文件
├── requirements.txt        # 依赖列表
└── README.md              # 说明文档
```

## 🔄 更新程序
1. 下载最新版本
2. 备份你的配置文件（如果需要）
3. 覆盖旧版本文件
4. 重新运行程序

## 📞 技术支持
如有问题，请访问项目GitHub页面：
https://github.com/luomodeshang/desktop-pet

或联系开发者：
- Email: 1024656097@qq.com
- GitHub: @luomodeshang
'''
    
    with open('README_Windows.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("✅ 已创建Windows使用说明")

def create_distribution_package():
    """创建分发包"""
    print("📦 正在创建分发包...")
    
    # 创建dist目录
    dist_dir = Path("dist/DesktopPet")
    dist_dir.mkdir(parents=True, exist_ok=True)
    
    # 复制必要文件
    files_to_copy = [
        ("src/main.py", "src/"),
        ("config/", "config/"),
        ("assets/images/", "assets/images/"),
        ("requirements.txt", "."),
        ("run.bat", "."),
        ("run.sh", "."),
        ("README.md", "."),
        ("process_photo_simple.py", "."),
    ]
    
    for src, dst in files_to_copy:
        src_path = Path(src)
        dst_path = dist_dir / dst
        
        if src.endswith('/'):
            # 复制目录
            if src_path.exists():
                shutil.copytree(src_path, dst_path / src_path.name, dirs_exist_ok=True)
                print(f"✅ 复制目录: {src}")
        else:
            # 复制文件
            if src_path.exists():
                dst_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_path, dst_path)
                print(f"✅ 复制文件: {src}")
    
    # 创建版本信息文件
    version_info = {
        "name": "DesktopPet",
        "version": "1.0.0",
        "author": "luomodeshang",
        "build_date": "2026-04-20",
        "github_url": "https://github.com/luomodeshang/desktop-pet"
    }
    
    with open(dist_dir / "version.json", 'w', encoding='utf-8') as f:
        json.dump(version_info, f, indent=2, ensure_ascii=False)
    
    print("✅ 分发包创建完成")
    return dist_dir

def main():
    """主函数"""
    print("=" * 50)
    print("       桌面宠物程序 - Windows打包工具")
    print("=" * 50)
    print()
    
    # 检查当前目录
    current_dir = Path.cwd()
    print(f"当前目录: {current_dir}")
    
    # 检查必要文件
    required_files = ["src/main.py", "requirements.txt", "config/settings.json"]
    for file in required_files:
        if not Path(file).exists():
            print(f"❌ 缺少必要文件: {file}")
            return
    
    print("✅ 所有必要文件都存在")
    
    # 创建打包目录
    packaging_dir = Path("packaging")
    packaging_dir.mkdir(exist_ok=True)
    
    # 创建各种文件
    create_spec_file()
    create_installer_script()
    create_readme_for_windows()
    
    # 创建分发包
    dist_dir = create_distribution_package()
    
    print()
    print("=" * 50)
    print("             打包完成！")
    print("=" * 50)
    print()
    print("📁 生成的文件：")
    print(f"1. 分发包目录: {dist_dir}")
    print("2. PyInstaller spec文件: desktop_pet.spec")
    print("3. 安装脚本: install.bat")
    print("4. Windows使用说明: README_Windows.md")
    print()
    print("🚀 下一步操作：")
    print("1. 在Windows电脑上安装Python和PyInstaller")
    print("2. 运行: pyinstaller desktop_pet.spec")
    print("3. 在dist/DesktopPet目录中找到可执行文件")
    print("4. 使用Inno Setup或NSIS创建安装程序")
    print()
    print("💡 提示：")
    print("- 确保Windows电脑已安装Microsoft Visual C++ Redistributable")
    print("- 首次运行可能需要几分钟时间编译")
    print("- 建议使用UPX压缩可执行文件大小")
    
    # 保存打包说明
    instructions = '''# Windows EXE打包指南

## 环境要求
1. Windows 10/11 操作系统
2. Python 3.8+ (64位)
3. Microsoft Visual C++ Redistributable

## 打包步骤

### 步骤1：准备环境
```cmd
# 安装Python（如果尚未安装）
# 访问 https://www.python.org/downloads/

# 安装必要工具
pip install pyinstaller
pip install -r requirements.txt
```

### 步骤2：运行打包脚本
```cmd
# 进入项目目录
cd desktop-pet

# 运行打包
pyinstaller desktop_pet.spec
```

### 步骤3：测试可执行文件
```cmd
# 进入输出目录
cd dist/DesktopPet

# 运行程序
DesktopPet.exe
```

### 步骤4：创建安装程序（可选）
使用 Inno Setup 或 NSIS 创建安装包：
1. 下载 Inno Setup: https://jrsoftware.org/isdl.php
2. 创建安装脚本
3. 编译生成 Setup.exe

## 文件说明
- `desktop_pet.spec` - PyInstaller配置文件
- `install.bat` - 自动安装脚本
- `README_Windows.md` - Windows用户指南
- `dist/DesktopPet/` - 打包输出目录

## 注意事项
1. 首次打包可能需要较长时间
2. 确保所有依赖项正确包含
3. 测试在不同Windows版本上的兼容性
4. 考虑使用代码签名证书（可选）

## 分发方式
1. 直接分发 `dist/DesktopPet` 目录
2. 创建ZIP压缩包
3. 使用安装程序（推荐）
4. 上传到GitHub Releases
'''
    
    with open(packaging_dir / "WINDOWS_PACKAGING_GUIDE.md", 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print(f"📄 详细打包指南已保存: {packaging_dir}/WINDOWS_PACKAGING_GUIDE.md")

if __name__ == "__main__":
    main()