#!/usr/bin/env python3
"""
为Windows用户构建EXE文件
目标：生成一个完全独立的可执行文件，无需Python环境
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def clean_build_dirs():
    """清理构建目录"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    files_to_clean = ['DesktopPet.spec']
    
    print("🧹 清理旧的构建文件...")
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"  已删除: {dir_name}")
    
    for file_name in files_to_clean:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"  已删除: {file_name}")

def check_requirements():
    """检查必要条件"""
    print("🔍 检查必要条件...")
    
    requirements = [
        ('src/main.py', '主程序文件'),
        ('assets/images/icon.ico', '程序图标'),
        ('config', '配置文件目录'),
        ('assets', '资源文件目录'),
    ]
    
    all_ok = True
    for path, desc in requirements:
        if os.path.exists(path):
            print(f"  ✅ {desc}: {path}")
        else:
            print(f"  ❌ {desc}不存在: {path}")
            all_ok = False
    
    return all_ok

def build_exe():
    """构建EXE文件"""
    print("🔨 开始构建EXE文件...")
    
    # PyInstaller命令
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--name=DesktopPet',
        '--onefile',           # 单个EXE文件
        '--windowed',          # 无控制台窗口
        '--clean',             # 清理临时文件
        '--noconfirm',         # 不询问确认
        f'--icon=assets/images/icon.ico',
        '--add-data=config:config',      # 包含config目录
        '--add-data=assets:assets',      # 包含assets目录
        '--hidden-import=PyQt5',
        '--hidden-import=PIL',
        '--hidden-import=cv2',
        '--hidden-import=numpy',
        'src/main.py'
    ]
    
    print(f"🚀 执行命令: {' '.join(cmd)}")
    
    try:
        # 运行PyInstaller
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ PyInstaller构建成功!")
            
            # 检查生成的EXE文件
            exe_path = 'dist/DesktopPet'
            if os.path.exists(exe_path):
                size_mb = os.path.getsize(exe_path) / (1024 * 1024)
                print(f"📦 EXE文件生成成功: {exe_path} ({size_mb:.2f} MB)")
                return True, exe_path
            else:
                print("❌ EXE文件未生成")
                return False, None
        else:
            print(f"❌ PyInstaller构建失败，返回码: {result.returncode}")
            print(f"标准输出:\n{result.stdout}")
            print(f"标准错误:\n{result.stderr}")
            return False, None
            
    except subprocess.TimeoutExpired:
        print("❌ 构建超时（5分钟）")
        return False, None
    except Exception as e:
        print(f"❌ 构建过程异常: {e}")
        return False, None

def create_windows_package(exe_path):
    """创建Windows用户包"""
    print("📦 创建Windows用户包...")
    
    package_dir = 'DesktopPet_Windows'
    
    # 创建目录结构
    os.makedirs(package_dir, exist_ok=True)
    
    # 复制EXE文件
    shutil.copy2(exe_path, f'{package_dir}/DesktopPet.exe')
    print(f"  ✅ 复制EXE文件到: {package_dir}/DesktopPet.exe")
    
    # 复制配置文件
    if os.path.exists('config'):
        shutil.copytree('config', f'{package_dir}/config', dirs_exist_ok=True)
        print(f"  ✅ 复制config目录")
    
    # 复制资源文件
    if os.path.exists('assets'):
        shutil.copytree('assets', f'{package_dir}/assets', dirs_exist_ok=True)
        print(f"  ✅ 复制assets目录")
    
    # 创建说明文件
    readme_content = """桌面宠物程序 - Windows版
==============================

🎮 使用方法：
1. 双击运行 DesktopPet.exe
2. 首次运行会提示选择一张照片
3. 选择照片后，桌面宠物就会出现！

🖱️ 操作说明：
- 左键点击宠物：触发动作（挥手、跳跃、踱步）
- 右键点击宠物：投喂食物（汉堡、炸鸡、螺蛳粉）
- 拖动宠物：可以移动位置
- 长时间不动：自动切换状态（站立→蹲下→睡觉）

⚠️ 注意事项：
1. 首次运行时，杀毒软件可能会报警，请点击"更多信息"→"仍要运行"
2. 程序会自动保存状态，下次打开会恢复
3. 需要关闭时，右键系统托盘图标选择退出

📁 文件说明：
- DesktopPet.exe：主程序
- config/：配置文件目录
- assets/：图片资源目录

🔧 技术支持：
- GitHub: https://github.com/luomodeshang/desktop-pet
- 邮箱: 1024656097@qq.com

版本: v1.0.5 (本地构建版)
构建时间: 2026-04-23
"""
    
    with open(f'{package_dir}/README.txt', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print(f"  ✅ 创建说明文件: {package_dir}/README.txt")
    
    # 创建ZIP包
    import zipfile
    zip_filename = 'DesktopPet_Windows_v1.0.5.zip'
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, package_dir)
                zipf.write(file_path, arcname)
    
    print(f"  ✅ 创建ZIP包: {zip_filename}")
    
    # 清理临时目录
    shutil.rmtree(package_dir)
    print(f"  🧹 清理临时目录: {package_dir}")
    
    return zip_filename

def main():
    """主函数"""
    print("=" * 60)
    print("       桌面宠物程序 - Windows EXE构建工具")
    print("=" * 60)
    print()
    
    # 1. 清理
    clean_build_dirs()
    
    # 2. 检查必要条件
    if not check_requirements():
        print("\n❌ 必要条件检查失败，请修复问题后重试")
        return
    
    print()
    
    # 3. 构建EXE
    success, exe_path = build_exe()
    
    if not success:
        print("\n❌ EXE构建失败")
        return
    
    print()
    
    # 4. 创建Windows用户包
    zip_file = create_windows_package(exe_path)
    
    print("\n" + "=" * 60)
    print("            🎉 构建完成！")
    print("=" * 60)
    print()
    print("📦 生成的文件：")
    print(f"   1. {exe_path} - 单个EXE文件 ({os.path.getsize(exe_path)/1024/1024:.1f} MB)")
    print(f"   2. {zip_file} - Windows用户包")
    print()
    print("📋 使用说明：")
    print("   1. 将 ZIP 包发送给Windows用户")
    print("   2. 用户解压后，双击 DesktopPet.exe 即可运行")
    print("   3. 无需安装Python或任何依赖")
    print()
    print("⚠️  注意事项：")
    print("   1. 杀毒软件可能误报，请指导用户点击'仍要运行'")
    print("   2. 首次运行需要选择一张照片")
    print("   3. 程序会自动保存状态")
    print()
    print("🔗 上传到GitHub：")
    print("   1. 访问: https://github.com/luomodeshang/desktop-pet/releases")
    print("   2. 点击'Draft a new release'")
    print("   3. 选择标签 v1.0.5 (或创建新标签)")
    print("   4. 上传这两个文件")
    print("   5. 发布即可！")

if __name__ == "__main__":
    main()