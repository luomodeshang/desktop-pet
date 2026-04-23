#!/usr/bin/env python3
"""
创建桌面宠物程序的发布包
"""

import os
import sys
import shutil
import zipfile
from pathlib import Path
import json
from datetime import datetime

def create_source_package():
    """创建源代码发布包"""
    print("📦 创建源代码发布包...")
    
    # 项目根目录
    project_root = Path.cwd()
    
    # 创建临时目录
    temp_dir = project_root / "temp_release"
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir()
    
    # 要包含的文件和目录
    include_patterns = [
        "src/",
        "assets/",
        "config/",
        "packaging/",
        "*.py",
        "*.md",
        "*.txt",
        "*.bat",
        "*.sh",
        ".github/",
    ]
    
    # 排除的文件和目录
    exclude_patterns = [
        "__pycache__",
        ".git",
        ".gitignore",
        "venv",
        "temp_*",
        "*.log",
        "*.tmp",
    ]
    
    # 复制文件
    files_copied = 0
    for pattern in include_patterns:
        if pattern.endswith('/'):
            # 目录模式
            dir_pattern = pattern.rstrip('/')
            for item in project_root.glob(dir_pattern):
                if item.is_dir():
                    # 检查是否在排除列表中
                    exclude = False
                    for exclude_pattern in exclude_patterns:
                        if exclude_pattern in str(item):
                            exclude = True
                            break
                    
                    if not exclude:
                        dest_dir = temp_dir / item.relative_to(project_root)
                        shutil.copytree(item, dest_dir, dirs_exist_ok=True)
                        files_copied += 1
                        print(f"✅ 复制目录: {item.name}")
        else:
            # 文件模式
            for item in project_root.glob(pattern):
                if item.is_file():
                    # 检查是否在排除列表中
                    exclude = False
                    for exclude_pattern in exclude_patterns:
                        if exclude_pattern in str(item):
                            exclude = True
                            break
                    
                    if not exclude:
                        dest_file = temp_dir / item.relative_to(project_root)
                        dest_file.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(item, dest_file)
                        files_copied += 1
                        print(f"✅ 复制文件: {item.name}")
    
    # 创建版本信息文件
    version_info = {
        "name": "DesktopPet",
        "version": "1.0.1",
        "release_date": datetime.now().strftime("%Y-%m-%d"),
        "author": "luomodeshang",
        "github_url": "https://github.com/luomodeshang/desktop-pet",
        "description": "桌面宠物程序 - 将你的照片变成会动的桌面宠物",
        "requirements": ["Python 3.8+", "Windows 10/11", "4GB RAM"],
        "included_files": files_copied
    }
    
    with open(temp_dir / "VERSION.json", 'w', encoding='utf-8') as f:
        json.dump(version_info, f, indent=2, ensure_ascii=False)
    
    # 创建ZIP文件
    zip_filename = project_root / "desktop-pet-v1.0.1-source.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(temp_dir)
                zipf.write(file_path, arcname)
    
    print(f"✅ 源代码包创建完成: {zip_filename}")
    
    # 清理临时目录
    shutil.rmtree(temp_dir)
    
    return zip_filename

def create_windows_package():
    """创建Windows用户包（不含Python环境）"""
    print("🖥️ 创建Windows用户包...")
    
    project_root = Path.cwd()
    
    # 创建临时目录
    temp_dir = project_root / "temp_windows"
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir()
    
    # Windows用户需要的文件
    windows_files = [
        ("src/main.py", "src/"),
        ("config/", "config/"),
        ("assets/images/", "assets/images/"),
        ("requirements.txt", "."),
        ("README_Windows.md", "README.md"),
        ("run.bat", "."),
        ("process_photo_simple.py", "."),
    ]
    
    # 复制文件
    for src, dst in windows_files:
        src_path = Path(src)
        dst_path = temp_dir / dst
        
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
    
    # 创建Windows专用说明
    windows_readme = """# 桌面宠物程序 - Windows版

## 🚀 快速开始

### 方法一：使用Python运行（需要安装Python）
1. 安装Python 3.8+（从 https://python.org 下载）
2. 打开命令提示符，进入本目录
3. 安装依赖：`pip install -r requirements.txt`
4. 运行程序：`python src/main.py`

### 方法二：使用批处理脚本
1. 双击 `run.bat` 文件
2. 如果提示安装Python，请先安装Python

## 🎮 基本操作

- **左键点击宠物**：触发动作（挥手、跳跃、踱步）
- **右键点击宠物**：显示投喂菜单
- **拖动宠物**：移动宠物位置
- **系统托盘图标**：右键退出程序

## 🖼️ 首次运行

1. 程序启动后会提示选择一张照片
2. 选择你的照片后，程序会自动生成动漫风格宠物
3. 宠物会显示在桌面右下角

## ⚙️ 配置说明

配置文件在 `config/` 目录中：
- `settings.json` - 程序设置
- `image_paths.json` - 图像路径

## 🛠️ 常见问题

### 1. 程序无法启动
- 确保已安装 Microsoft Visual C++ Redistributable
- 尝试以管理员身份运行
- 检查杀毒软件是否误报

### 2. 照片处理失败
- 确保照片格式为 JPG/PNG
- 照片大小建议 500x500 像素以上
- 避免使用过大的照片

## 📞 技术支持

GitHub: https://github.com/luomodeshang/desktop-pet
Email: 1024656097@qq.com

---
版本: 1.0.1 | 更新日期: 2026年4月23日
"""
    
    with open(temp_dir / "WINDOWS_README.txt", 'w', encoding='utf-8') as f:
        f.write(windows_readme)
    
    # 创建版本信息
    version_info = {
        "name": "DesktopPet",
        "version": "1.0.1",
        "platform": "Windows",
        "python_required": "3.8+",
        "release_date": datetime.now().strftime("%Y-%m-%d"),
        "note": "此包为Windows用户准备，需要自行安装Python环境"
    }
    
    with open(temp_dir / "VERSION.json", 'w', encoding='utf-8') as f:
        json.dump(version_info, f, indent=2, ensure_ascii=False)
    
    # 创建ZIP文件
    zip_filename = project_root / "desktop-pet-v1.0.1-windows.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(temp_dir)
                zipf.write(file_path, arcname)
    
    print(f"✅ Windows用户包创建完成: {zip_filename}")
    
    # 清理临时目录
    shutil.rmtree(temp_dir)
    
    return zip_filename

def create_github_release_assets():
    """创建GitHub Release需要的所有资源文件"""
    print("🚀 创建GitHub Release资源文件...")
    
    project_root = Path.cwd()
    release_dir = project_root / "release_assets"
    release_dir.mkdir(exist_ok=True)
    
    # 1. 创建源代码包
    source_zip = create_source_package()
    if source_zip.exists():
        shutil.copy2(source_zip, release_dir / source_zip.name)
    
    # 2. 创建Windows用户包
    windows_zip = create_windows_package()
    if windows_zip.exists():
        shutil.copy2(windows_zip, release_dir / windows_zip.name)
    
    # 3. 复制发布说明
    release_notes = project_root / "RELEASE_v1.0.1.md"
    if release_notes.exists():
        shutil.copy2(release_notes, release_dir / "RELEASE_NOTES.md")
    
    # 4. 创建下载说明
    download_guide = """# 桌面宠物程序 v1.0.1 下载指南

## 📥 下载链接

### 1. 完整源代码包
- **desktop-pet-v1.0.1-source.zip** - 包含所有源代码和资源文件
- 适合开发者或想要自定义功能的用户
- 需要自行安装Python和依赖

### 2. Windows用户包
- **desktop-pet-v1.0.1-windows.zip** - 专为Windows用户准备
- 包含运行所需的所有文件
- 需要安装Python 3.8+环境

## 🔧 安装说明

### 对于开发者/高级用户
1. 下载 **desktop-pet-v1.0.1-source.zip**
2. 解压到任意目录
3. 安装Python依赖：`pip install -r requirements.txt`
4. 运行：`python src/main.py`

### 对于Windows普通用户
1. 下载 **desktop-pet-v1.0.1-windows.zip**
2. 解压到任意目录
3. 确保已安装Python 3.8+
4. 双击 `run.bat` 或运行 `python src/main.py`

## 🎯 版本亮点

### v1.0.1 新增功能
- ✅ 完整的打包脚本支持
- ✅ Windows专用文档和指南
- ✅ GitHub Actions自动构建工作流
- ✅ 改进的用户体验和错误处理

### 系统要求
- **操作系统**: Windows 10/11
- **Python版本**: 3.8+（Windows用户包需要）
- **内存**: 4GB RAM（推荐8GB）
- **存储空间**: 200MB可用空间

## 📞 技术支持

- **GitHub Issues**: https://github.com/luomodeshang/desktop-pet/issues
- **Email**: 1024656097@qq.com
- **文档**: 查看包内的README文件

## 🔄 更新日志

详细更新内容请查看 RELEASE_NOTES.md 文件

---
**祝你使用愉快！** 🐾

*版本: v1.0.1 | 发布日期: 2026年4月23日*
"""
    
    with open(release_dir / "DOWNLOAD_GUIDE.md", 'w', encoding='utf-8') as f:
        f.write(download_guide)
    
    print(f"✅ Release资源文件已创建到: {release_dir}")
    print()
    print("📁 生成的文件:")
    for file in release_dir.iterdir():
        print(f"  - {file.name} ({file.stat().st_size / 1024:.1f} KB)")
    
    return release_dir

def main():
    """主函数"""
    print("=" * 50)
    print("       桌面宠物程序 - 发布包创建工具")
    print("=" * 50)
    print()
    
    print("请选择要创建的包类型:")
    print("1. 源代码包 (适合开发者)")
    print("2. Windows用户包 (需要Python环境)")
    print("3. 所有Release资源文件 (GitHub发布)")
    print("4. 全部创建")
    print()
    
    try:
        choice = input("请输入选择 (1-4): ").strip()
        
        if choice == "1":
            create_source_package()
        elif choice == "2":
            create_windows_package()
        elif choice == "3":
            create_github_release_assets()
        elif choice == "4":
            create_source_package()
            create_windows_package()
            release_dir = create_github_release_assets()
            print()
            print("🎉 所有包已创建完成！")
            print(f"📂 Release资源目录: {release_dir}")
        else:
            print("❌ 无效选择")
            return
    except KeyboardInterrupt:
        print("\n\n操作已取消")
        return
    except Exception as e:
        print(f"❌ 创建失败: {e}")
        return
    
    print()
    print("=" * 50)
    print("             创建完成！")
    print("=" * 50)
    print()
    print("🚀 下一步:")
    print("1. 将生成的ZIP文件上传到GitHub Releases")
    print("2. 在GitHub上创建新的Release")
    print("3. 添加发布说明和下载链接")
    print("4. 分享Release链接给用户")
    print()
    print("💡 提示:")
    print("- 源代码包适合开发者")
    print("- Windows用户包需要用户安装Python")
    print("- 考虑未来添加自动构建的EXE文件")

if __name__ == "__main__":
    main()