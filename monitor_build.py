#!/usr/bin/env python3
"""
监控GitHub Actions构建状态
"""

import requests
import time
import json
from datetime import datetime

def check_build_status(owner="luomodeshang", repo="desktop-pet", tag="v1.0.4"):
    """检查构建状态"""
    print(f"🔍 检查 {owner}/{repo} 标签 {tag} 的构建状态...")
    
    # 检查工作流运行
    runs_url = f"https://api.github.com/repos/{owner}/{repo}/actions/runs"
    
    try:
        response = requests.get(runs_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            # 查找与标签相关的最新运行
            workflow_runs = data.get("workflow_runs", [])
            
            # 查找简化版工作流的运行
            simple_runs = [run for run in workflow_runs if "simple" in run.get("name", "").lower()]
            
            if simple_runs:
                latest_run = simple_runs[0]
                print(f"📋 最新简化版构建:")
                print(f"   工作流: {latest_run.get('name', 'N/A')}")
                print(f"   状态: {latest_run.get('status', 'N/A')}")
                print(f"   结论: {latest_run.get('conclusion', 'N/A')}")
                print(f"   触发时间: {latest_run.get('created_at', 'N/A')}")
                print(f"   运行ID: {latest_run.get('id', 'N/A')}")
                print(f"   详情链接: {latest_run.get('html_url', 'N/A')}")
                
                # 检查运行日志
                if latest_run.get('status') == 'completed':
                    if latest_run.get('conclusion') == 'success':
                        print("🎉 构建成功!")
                        return True, latest_run
                    else:
                        print("❌ 构建失败")
                        return False, latest_run
                else:
                    print("⏳ 构建进行中...")
                    return None, latest_run
            else:
                print("⚠️ 没有找到简化版工作流的运行记录")
                return None, None
        else:
            print(f"❌ API请求失败: {response.status_code}")
            return None, None
            
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        return None, None

def check_release(owner="luomodeshang", repo="desktop-pet", tag="v1.0.4"):
    """检查Release"""
    print(f"\n📦 检查Release {tag}...")
    
    release_url = f"https://api.github.com/repos/{owner}/{repo}/releases/tags/{tag}"
    
    try:
        response = requests.get(release_url, timeout=10)
        if response.status_code == 200:
            release_data = response.json()
            
            print(f"✅ Release {tag} 已创建!")
            print(f"   标题: {release_data.get('name', 'N/A')}")
            print(f"   发布日期: {release_data.get('published_at', 'N/A')}")
            
            # 检查文件
            assets = release_data.get('assets', [])
            if assets:
                print(f"\n📁 可用文件 ({len(assets)}个):")
                for asset in assets:
                    print(f"   - {asset['name']} ({asset.get('download_count', 0)}次下载)")
                    print(f"     大小: {int(asset['size'])/1024/1024:.2f} MB")
                    print(f"     下载: {asset['browser_download_url']}")
                return True, release_data
            else:
                print("⚠️ Release已创建，但还没有文件上传")
                return True, release_data
        elif response.status_code == 404:
            print("⏳ Release尚未创建")
            return False, None
        else:
            print(f"❓ API请求状态: {response.status_code}")
            return False, None
            
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        return False, None

def monitor_build(interval=30, max_checks=20):
    """监控构建状态"""
    print("=" * 60)
    print("       GitHub Actions构建监控")
    print("=" * 60)
    print()
    
    checks = 0
    build_success = None
    
    while checks < max_checks:
        checks += 1
        print(f"\n📊 第 {checks} 次检查 ({datetime.now().strftime('%H:%M:%S')})")
        print("-" * 40)
        
        # 检查构建状态
        build_status, run_info = check_build_status()
        
        # 检查Release
        release_exists, release_info = check_release()
        
        # 判断是否完成
        if build_status is True and release_exists:
            print("\n🎉 构建和Release都已完成!")
            print(f"   下载链接: https://github.com/luomodeshang/desktop-pet/releases/tag/v1.0.4")
            build_success = True
            break
        elif build_status is False:
            print("\n❌ 构建失败，请查看日志")
            if run_info:
                print(f"   日志链接: {run_info.get('html_url', '')}/jobs")
            build_success = False
            break
        elif release_exists:
            print("\n✅ Release已创建，等待文件上传...")
        else:
            print(f"\n⏳ 等待 {interval} 秒后再次检查...")
            time.sleep(interval)
    
    print("\n" + "=" * 60)
    print("                监控结束")
    print("=" * 60)
    
    if build_success is True:
        print("\n✅ 构建成功!")
        print("   Windows用户现在可以下载EXE文件:")
        print("   https://github.com/luomodeshang/desktop-pet/releases/tag/v1.0.4")
    elif build_success is False:
        print("\n❌ 构建失败")
        print("   请查看GitHub Actions日志:")
        print("   https://github.com/luomodeshang/desktop-pet/actions")
    else:
        print("\n⏳ 构建超时，请手动检查:")
        print("   https://github.com/luomodeshang/desktop-pet/actions")
    
    return build_success

if __name__ == "__main__":
    # 开始监控
    monitor_build(interval=30, max_checks=20)