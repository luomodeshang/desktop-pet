#!/usr/bin/env python3
"""
检查GitHub Actions构建状态和Release文件
"""

import requests
import json
import time
from datetime import datetime

def check_github_actions():
    """检查GitHub Actions构建状态"""
    print("🔍 检查GitHub Actions构建状态...")
    
    api_url = "https://api.github.com/repos/luomodeshang/desktop-pet/actions/runs"
    
    try:
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("workflow_runs"):
                latest_run = data["workflow_runs"][0]
                
                print(f"📋 最新构建:")
                print(f"   工作流: {latest_run.get('name', 'N/A')}")
                print(f"   状态: {latest_run.get('status', 'N/A')}")
                print(f"   结论: {latest_run.get('conclusion', 'N/A')}")
                print(f"   触发时间: {latest_run.get('created_at', 'N/A')}")
                print(f"   运行ID: {latest_run.get('id', 'N/A')}")
                
                # 构建详情链接
                html_url = latest_run.get('html_url', '')
                if html_url:
                    print(f"   详情链接: {html_url}")
                
                return latest_run
            else:
                print("❌ 没有找到构建记录")
                return None
        else:
            print(f"❌ API请求失败: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        return None

def check_release_files():
    """检查Release文件是否已生成"""
    print("\n📦 检查Release文件...")
    
    release_url = "https://api.github.com/repos/luomodeshang/desktop-pet/releases/tags/v1.0.2"
    
    try:
        response = requests.get(release_url, timeout=10)
        if response.status_code == 200:
            release_data = response.json()
            
            print(f"🎉 Release v1.0.2 已创建!")
            print(f"   标题: {release_data.get('name', 'N/A')}")
            print(f"   发布日期: {release_data.get('published_at', 'N/A')}")
            print(f"   下载次数: {release_data.get('download_count', 0)}")
            
            # 检查文件
            assets = release_data.get('assets', [])
            if assets:
                print(f"\n📁 可用文件 ({len(assets)}个):")
                for asset in assets:
                    print(f"   - {asset['name']} ({asset.get('download_count', 0)}次下载)")
                    print(f"     大小: {int(asset['size'])/1024/1024:.2f} MB")
                    print(f"     下载: {asset['browser_download_url']}")
            else:
                print("⚠️ 还没有文件上传到Release")
                
            return release_data
        elif response.status_code == 404:
            print("⚠️ Release v1.0.2 尚未创建或正在构建中")
            return None
        else:
            print(f"❌ API请求失败: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        return None

def check_direct_downloads():
    """检查直接下载链接是否可用"""
    print("\n🔗 检查直接下载链接...")
    
    files_to_check = [
        ("DesktopPet.exe", "https://github.com/luomodeshang/desktop-pet/releases/download/v1.0.2/DesktopPet.exe"),
        ("DesktopPet_Windows_v1.0.2.zip", "https://github.com/luomodeshang/desktop-pet/releases/download/v1.0.2/DesktopPet_Windows_v1.0.2.zip"),
        ("DesktopPet_Setup.exe", "https://github.com/luomodeshang/desktop-pet/releases/download/v1.0.2/DesktopPet_Setup.exe"),
    ]
    
    available_files = []
    
    for filename, url in files_to_check:
        try:
            # 发送HEAD请求检查文件是否存在
            response = requests.head(url, timeout=5, allow_redirects=True)
            if response.status_code == 200:
                size = response.headers.get('content-length', '未知')
                if size != '未知':
                    size_mb = int(size) / 1024 / 1024
                    print(f"✅ {filename} - 可用 ({size_mb:.2f} MB)")
                else:
                    print(f"✅ {filename} - 可用")
                available_files.append(filename)
            elif response.status_code == 404:
                print(f"⏳ {filename} - 尚未生成")
            else:
                print(f"❓ {filename} - 状态码: {response.status_code}")
        except Exception as e:
            print(f"❌ {filename} - 检查失败: {e}")
    
    return available_files

def main():
    """主函数"""
    print("=" * 60)
    print("       桌面宠物程序 - 构建状态检查工具")
    print("=" * 60)
    print()
    
    print("📊 检查项目: luomodeshang/desktop-pet")
    print("🏷️  目标版本: v1.0.2")
    print()
    
    # 检查构建状态
    build_info = check_github_actions()
    
    # 检查Release
    release_info = check_release_files()
    
    # 检查直接下载
    available_files = check_direct_downloads()
    
    print("\n" + "=" * 60)
    print("                检查结果汇总")
    print("=" * 60)
    
    if release_info:
        print("✅ Release已创建，可以访问:")
        print(f"   https://github.com/luomodeshang/desktop-pet/releases/tag/v1.0.2")
        
        if available_files:
            print(f"\n✅ {len(available_files)}个文件已就绪，Windows用户可直接下载使用")
            print("   推荐下载: DesktopPet.exe (单个文件，最简单)")
        else:
            print("\n⏳ 文件正在上传中，请稍后刷新页面")
    else:
        print("⏳ Release尚未创建，GitHub Actions正在构建中")
        print("   请稍后访问: https://github.com/luomodeshang/desktop-pet/actions")
    
    print("\n💡 用户指南:")
    print("1. Windows用户: 下载EXE文件，双击即可运行")
    print("2. 遇到杀毒软件报警: 点击'更多信息'→'仍要运行'")
    print("3. 首次运行: 选择一张照片生成宠物")
    print("4. 详细教程: 查看 WINDOWS_USER_GUIDE_EXE.md")
    
    print("\n🔄 自动刷新:")
    print("   此检查不会自动刷新，请手动:")
    print("   1. 等待5-10分钟让构建完成")
    print("   2. 刷新GitHub Releases页面")
    print("   3. 重新运行此脚本检查状态")
    
    print("\n📞 如有问题:")
    print("   - GitHub Issues: https://github.com/luomodeshang/desktop-pet/issues")
    print("   - Email: 1024656097@qq.com")

if __name__ == "__main__":
    main()