#!/usr/bin/env python3
"""
测试PyInstaller构建
"""

import os
import subprocess
import sys

def test_pyinstaller():
    """测试PyInstaller构建"""
    print("🔧 测试PyInstaller构建...")
    
    # 检查源文件
    main_py = "src/main.py"
    if not os.path.exists(main_py):
        print(f"❌ 找不到主文件: {main_py}")
        return False
    
    print(f"✅ 找到主文件: {main_py}")
    
    # 检查图标文件
    icon_file = "assets/images/icon.ico"
    if not os.path.exists(icon_file):
        print(f"❌ 找不到图标文件: {icon_file}")
        return False
    
    print(f"✅ 找到图标文件: {icon_file}")
    
    # 清理旧的构建文件
    for dir_name in ["build", "dist"]:
        if os.path.exists(dir_name):
            print(f"🧹 清理旧的 {dir_name} 目录...")
            import shutil
            shutil.rmtree(dir_name)
    
    # 构建命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--clean",
        "--noconfirm",
        "--name=DesktopPet",
        "--onefile",
        "--windowed",
        f"--icon={icon_file}",
        "--add-data=config:config",
        "--add-data=assets:assets",
        "--hidden-import=PyQt5",
        "--hidden-import=PIL",
        "--hidden-import=cv2",
        "--hidden-import=numpy",
        main_py
    ]
    
    print(f"🚀 运行命令: {' '.join(cmd)}")
    
    try:
        # 运行PyInstaller
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ PyInstaller构建成功!")
            
            # 检查生成的EXE文件
            exe_path = "dist/DesktopPet"
            if os.path.exists(exe_path):
                size = os.path.getsize(exe_path) / (1024 * 1024)
                print(f"📦 EXE文件生成成功: {exe_path} ({size:.2f} MB)")
                return True
            else:
                print("❌ EXE文件未生成")
                return False
        else:
            print(f"❌ PyInstaller构建失败，返回码: {result.returncode}")
            print(f"标准输出:\n{result.stdout}")
            print(f"标准错误:\n{result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ PyInstaller构建超时")
        return False
    except Exception as e:
        print(f"❌ 构建过程异常: {e}")
        return False

def check_dependencies():
    """检查依赖"""
    print("🔍 检查依赖...")
    
    dependencies = [
        ("PyQt5", "PyQt5"),
        ("PIL", "PIL"),
        ("OpenCV", "cv2"),
        ("NumPy", "numpy"),
        ("PyInstaller", "PyInstaller"),
    ]
    
    all_ok = True
    for name, module in dependencies:
        try:
            __import__(module)
            print(f"✅ {name} 已安装")
        except ImportError as e:
            print(f"❌ {name} 未安装: {e}")
            all_ok = False
    
    return all_ok

def main():
    """主函数"""
    print("=" * 60)
    print("       桌面宠物程序 - 构建测试")
    print("=" * 60)
    print()
    
    # 检查依赖
    if not check_dependencies():
        print("\n⚠️  依赖检查失败，请先安装缺失的依赖")
        return
    
    print("\n" + "=" * 60)
    
    # 测试构建
    if test_pyinstaller():
        print("\n🎉 构建测试成功!")
        print("   生成的EXE文件在: dist/DesktopPet")
        print("   可以上传到GitHub Actions进行完整构建")
    else:
        print("\n❌ 构建测试失败")
        print("   请检查错误信息并修复问题")
    
    print("\n📋 下一步:")
    print("   1. 修复发现的任何问题")
    print("   2. 重新推送标签触发GitHub Actions")
    print("   3. 或手动运行: git tag -a v1.0.3 -m '修复构建问题'")
    print("   4. git push origin v1.0.3")

if __name__ == "__main__":
    main()