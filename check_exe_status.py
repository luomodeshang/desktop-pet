#!/usr/bin/env python3
"""
检查Windows EXE是否已发布
"""

import requests
import time
from datetime import datetime

def check_exe_available():
    """检查EXE文件是否可用"""
    print("🔍 检查DesktopPet.exe是否已发布...")
    
    # 直接检查EXE下载链接
    exe_url = "https://github.com/luomodeshang/desktop-pet/releases/latest/download/DesktopPet.exe"
    
    try:
        # 发送HEAD请求检查文件是否存在
        response = requests.head(exe_url, timeout=10, allow_redirects=True)
        
        if response.status_code == 200:
            size = response.headers.get('content-length', '未知')
            if size != '未知':
                size_mb = int(size) / 1024 / 1024
                print(f"✅ DesktopPet.exe 已发布！ ({size_mb:.1f} MB)")
                print(f"   下载链接: {exe_url}")
                return True, size_mb
            else:
                print(f"✅ DesktopPet.exe 已发布！")
                print(f"   下载链接: {exe_url}")
                return True, 0
        elif response.status_code == 404:
            print("⏳ DesktopPet.exe 尚未发布")
            return False, 0
        else:
            print(f"❓ 检查失败，状态码: {response.status_code}")
            return False, 0
            
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        return False, 0

def check_github_actions():
    """检查GitHub Actions状态"""
    print("\n🔧 检查GitHub Actions构建状态...")
    
    api_url = "https://api.github.com/repos/luomodeshang/desktop-pet/actions/runs"
    
    try:
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            workflow_runs = data.get("workflow_runs", [])
            
            # 查找最新的构建
            fixed_builds = [run for run in workflow_runs if "fixed" in run.get("name", "").lower()]
            
            if fixed_builds:
                latest = fixed_builds[0]
                print(f"📋 最新构建: {latest.get('name', 'N/A')}")
                print(f"   状态: {latest.get('status', 'N/A')}")
                print(f"   结论: {latest.get('conclusion', 'N/A')}")
                print(f"   开始时间: {latest.get('created_at', 'N/A')}")
                
                if latest.get('status') == 'completed':
                    if latest.get('conclusion') == 'success':
                        print("🎉 构建成功！")
                        return True
                    else:
                        print("❌ 构建失败")
                        return False
                else:
                    print("⏳ 构建进行中...")
                    return None
            else:
                print("⚠️ 没有找到构建记录")
                return None
        else:
            print(f"❌ API请求失败: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        return None

def main():
    """主函数"""
    print("=" * 60)
    print("       Windows EXE发布状态检查")
    print("=" * 60)
    print()
    
    print("📊 项目: luomodeshang/desktop-pet")
    print("🏷️  最新标签: v1.0.5")
    print("⏰ 检查时间:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print()
    
    # 检查EXE是否可用
    exe_available, size_mb = check_exe_available()
    
    # 检查构建状态
    build_status = check_github_actions()
    
    print("\n" + "=" * 60)
    print("                检查结果")
    print("=" * 60)
    
    if exe_available:
        print("\n🎉 **EXE文件已就绪！**")
        print()
        print("📥 下载链接:")
        print("   https://github.com/luomodeshang/desktop-pet/releases/latest/download/DesktopPet.exe")
        print()
        print("📋 使用方法:")
        print("   1. 下载 DesktopPet.exe")
        print("   2. 双击运行（杀毒软件可能报警，点击'仍要运行'）")
        print("   3. 选择一张照片生成宠物")
        print("   4. 开始互动！")
    else:
        print("\n⏳ **EXE文件尚未发布**")
        print()
        print("📋 当前状态:")
        if build_status is True:
            print("   ✅ GitHub Actions构建成功")
            print("   ⏳ 等待文件上传到Release...")
        elif build_status is False:
            print("   ❌ GitHub Actions构建失败")
            print("   请查看: https://github.com/luomodeshang/desktop-pet/actions")
        else:
            print("   ⏳ GitHub Actions构建进行中")
            print("   预计需要5-10分钟完成")
        
        print()
        print("💡 临时解决方案:")
        print("   1. 使用 'Windows_用户助手.bat' 脚本")
        print("   2. 或手动安装Python运行源码版")
        print("   3. 详细指南: WINDOWS_USER_GUIDE_EXE.md")
    
    print("\n🔗 相关链接:")
    print("   - GitHub Releases: https://github.com/luomodeshang/desktop-pet/releases")
    print("   - GitHub Actions: https://github.com/luomodeshang/desktop-pet/actions")
    print("   - 用户指南: WINDOWS_USER_GUIDE_EXE.md")
    
    print("\n🔄 自动刷新:")
    print("   此检查不会自动刷新，建议:")
    print("   1. 等待10分钟后刷新GitHub页面")
    print("   2. 或重新运行此脚本检查状态")

if __name__ == "__main__":
    main()