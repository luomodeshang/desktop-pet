#!/usr/bin/env python3
"""
将PNG图像转换为ICO图标文件
"""

import os
import sys
from PIL import Image

def convert_png_to_ico(png_path, ico_path, sizes=None):
    """
    将PNG图像转换为ICO图标
    
    Args:
        png_path: 输入的PNG文件路径
        ico_path: 输出的ICO文件路径
        sizes: ICO包含的尺寸列表，默认[16, 32, 48, 64, 128, 256]
    """
    if sizes is None:
        sizes = [16, 32, 48, 64, 128, 256]
    
    try:
        # 打开原始图像
        img = Image.open(png_path)
        
        # 创建不同尺寸的图像
        images = []
        for size in sizes:
            # 调整尺寸并保持透明通道
            resized = img.resize((size, size), Image.Resampling.LANCZOS)
            
            # 确保图像有透明通道（如果是RGBA）
            if img.mode == 'RGBA':
                resized = resized.convert('RGBA')
            else:
                # 如果没有透明通道，转换为RGBA并添加不透明alpha
                resized = resized.convert('RGBA')
            
            images.append(resized)
        
        # 保存为ICO
        images[0].save(
            ico_path,
            format='ICO',
            sizes=[(img.width, img.height) for img in images],
            append_images=images[1:] if len(images) > 1 else []
        )
        
        print(f"✅ ICO图标创建成功: {ico_path}")
        print(f"   包含尺寸: {sizes}")
        
        # 显示文件信息
        ico_size = os.path.getsize(ico_path) / 1024
        print(f"   文件大小: {ico_size:.1f} KB")
        
        return True
        
    except Exception as e:
        print(f"❌ 转换失败: {e}")
        return False

def create_default_icon():
    """创建默认的ICO图标"""
    # 使用cartoon_pet.png作为源
    png_path = "assets/images/cartoon_pet.png"
    ico_path = "assets/images/icon.ico"
    
    if not os.path.exists(png_path):
        print(f"❌ 源PNG文件不存在: {png_path}")
        
        # 创建一个简单的默认图标
        print("🔄 创建默认图标...")
        try:
            # 创建一个简单的红色心形图标
            from PIL import Image, ImageDraw
            
            # 创建256x256的图像
            img = Image.new('RGBA', (256, 256), (255, 255, 255, 0))
            draw = ImageDraw.Draw(img)
            
            # 绘制一个简单的心形
            # 使用两个椭圆和一个三角形组成心形
            # 上部分：两个半圆
            draw.ellipse([64, 30, 192, 158], fill=(255, 105, 180, 255))  # 左半圆
            draw.ellipse([128, 30, 256, 158], fill=(255, 105, 180, 255))  # 右半圆
            
            # 下部分：三角形
            draw.polygon(
                [(64, 94), (256, 94), (160, 256)],
                fill=(255, 105, 180, 255)
            )
            
            # 保存为PNG
            temp_png = "temp_icon.png"
            img.save(temp_png)
            
            # 转换为ICO
            convert_png_to_ico(temp_png, ico_path)
            
            # 清理临时文件
            os.remove(temp_png)
            
            return True
            
        except Exception as e:
            print(f"❌ 创建默认图标失败: {e}")
            return False
    
    # 转换现有的PNG为ICO
    return convert_png_to_ico(png_path, ico_path)

def main():
    """主函数"""
    print("=" * 50)
    print("       桌面宠物程序 - ICO图标生成工具")
    print("=" * 50)
    print()
    
    # 检查PIL是否安装
    try:
        from PIL import Image
    except ImportError:
        print("❌ 需要安装Pillow库")
        print("   运行: pip install Pillow")
        return
    
    # 创建默认图标
    print("🔄 正在创建ICO图标...")
    if create_default_icon():
        print()
        print("🎉 ICO图标创建完成！")
        print()
        print("📁 图标位置: assets/images/icon.ico")
        print()
        print("💡 使用方法:")
        print("1. 在PyInstaller中使用: --icon=\"assets/images/icon.ico\"")
        print("2. 在Windows中显示为程序图标")
        print("3. 在任务栏和桌面快捷方式中显示")
    else:
        print("❌ ICO图标创建失败")
        print()
        print("⚠️ 替代方案:")
        print("1. 手动创建ICO文件")
        print("2. 使用在线转换工具: https://convertio.co/zh/png-ico/")
        print("3. 修改GitHub Actions工作流，移除--icon参数")

if __name__ == "__main__":
    main()