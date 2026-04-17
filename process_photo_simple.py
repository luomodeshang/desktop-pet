#!/usr/bin/env python3
"""
简化的照片处理程序（不依赖OpenCV）
"""

import os
from PIL import Image, ImageFilter, ImageDraw, ImageFont
import json

def simple_cartoonize_pil(input_path, output_path, size=(256, 256)):
    """
    使用PIL进行简化的卡通化
    """
    print(f"处理照片: {input_path}")
    
    try:
        # 打开图像
        img = Image.open(input_path)
        print(f"原始尺寸: {img.size}, 模式: {img.mode}")
        
        # 调整大小
        img = img.resize(size, Image.Resampling.LANCZOS)
        
        # 方法1: 转换为卡通风格
        # 1. 边缘检测（使用查找边缘滤镜）
        edges = img.filter(ImageFilter.FIND_EDGES)
        
        # 2. 颜色简化（减少颜色数量）
        # 先转换为调色板图像
        img_palette = img.convert('P', palette=Image.Palette.ADAPTIVE, colors=16)
        
        # 转换回RGB
        img_simple = img_palette.convert('RGB')
        
        # 3. 稍微模糊以创建卡通效果
        img_blur = img_simple.filter(ImageFilter.GaussianBlur(radius=1))
        
        # 4. 增强对比度
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Contrast(img_blur)
        img_enhanced = enhancer.enhance(1.3)
        
        # 5. 合并边缘（可选）
        # 创建最终图像
        final_img = img_enhanced
        
        # 保存结果
        final_img.save(output_path, 'PNG')
        
        print(f"✅ 卡通化完成: {output_path}")
        print(f"  文件大小: {os.path.getsize(output_path) / 1024:.1f} KB")
        
        return True
        
    except Exception as e:
        print(f"❌ 处理失败: {e}")
        return False

def create_simple_pet_images(cartoon_path):
    """
    创建简单的宠物状态图像
    """
    print("\n创建宠物状态图像...")
    
    try:
        # 读取卡通图像
        base_img = Image.open(cartoon_path)
        
        # 创建不同状态的图像
        states = {}
        
        # 1. 站立状态（原图）
        states["standing"] = base_img.copy()
        
        # 2. 蹲下状态（缩小并变形）
        crouching = base_img.copy()
        # 调整大小（变矮）
        new_size = (crouching.width, int(crouching.height * 0.8))
        crouching = crouching.resize(new_size, Image.Resampling.LANCZOS)
        states["crouching"] = crouching
        
        # 3. 睡眠状态（旋转并添加文字）
        sleeping = base_img.copy()
        # 旋转90度
        sleeping = sleeping.rotate(90, expand=True)
        # 调整大小
        sleeping = sleeping.resize(
            (int(sleeping.width * 0.7), int(sleeping.height * 0.7)),
            Image.Resampling.LANCZOS
        )
        
        # 添加ZZZ文字
        try:
            draw = ImageDraw.Draw(sleeping)
            # 尝试使用默认字体
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
            except:
                font = ImageFont.load_default()
            
            draw.text((10, 10), "Zzz", fill=(255, 0, 0), font=font)
        except:
            pass  # 如果添加文字失败，继续
            
        states["sleeping"] = sleeping
        
        # 保存所有状态图像
        for state_name, state_img in states.items():
            output_path = f"assets/images/pet_{state_name}.png"
            state_img.save(output_path, 'PNG')
            print(f"  ✅ 已保存: {output_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ 创建状态图像失败: {e}")
        return False

def create_food_images():
    """
    创建食物图像（使用emoji或简单图形）
    """
    print("\n创建食物图像...")
    
    foods = ["汉堡", "炸鸡", "螺蛳粉"]
    food_emojis = {"汉堡": "🍔", "炸鸡": "🍗", "螺蛳粉": "🍜"}
    
    os.makedirs("assets/images/foods", exist_ok=True)
    
    for food in foods:
        # 创建简单的食物图像
        img = Image.new('RGBA', (64, 64), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        # 绘制简单的食物图形
        if food == "汉堡":
            # 汉堡：棕色矩形
            draw.rectangle([10, 20, 54, 30], fill=(139, 69, 19))  # 肉饼
            draw.rectangle([5, 15, 59, 20], fill=(255, 223, 186))  # 面包上
            draw.rectangle([5, 30, 59, 35], fill=(255, 223, 186))  # 面包下
            
        elif food == "炸鸡":
            # 炸鸡：黄色不规则形状
            draw.ellipse([15, 15, 49, 49], fill=(255, 215, 0))
            
        elif food == "螺蛳粉":
            # 面条：黄色波浪线
            for i in range(5):
                y = 15 + i * 8
                draw.line([10, y, 54, y], fill=(255, 165, 0), width=3)
        
        # 保存
        output_path = f"assets/images/foods/{food}.png"
        img.save(output_path, 'PNG')
        print(f"  ✅ 已创建: {output_path}")
    
    return True

def update_main_program():
    """
    更新主程序以使用生成的图像
    """
    print("\n更新主程序配置...")
    
    # 更新配置文件
    config = {
        "images": {
            "pet_standing": "assets/images/pet_standing.png",
            "pet_crouching": "assets/images/pet_crouching.png", 
            "pet_sleeping": "assets/images/pet_sleeping.png",
            "foods": {
                "汉堡": "assets/images/foods/汉堡.png",
                "炸鸡": "assets/images/foods/炸鸡.png",
                "螺蛳粉": "assets/images/foods/螺蛳粉.png"
            }
        }
    }
    
    with open("config/image_paths.json", "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print("✅ 配置文件已更新")
    
    # 创建简单的README
    readme = """# 桌面宠物程序

## 功能特性
- 使用你的照片生成动漫风格宠物
- 右键投喂（汉堡、炸鸡、螺蛳粉）
- 左键点击触发动作（挥手、跳跃、踱步）
- 闲置时自动切换状态（站立→蹲下→睡眠）
- 状态自动保存

## 使用方法
1. 安装依赖：`pip install -r requirements.txt`
2. 处理照片：`python process_photo_simple.py`
3. 启动程序：`python src/main.py`

## 文件结构
- `src/main.py` - 主程序
- `process_photo_simple.py` - 照片处理
- `assets/images/` - 图像资源
- `config/` - 配置文件

## 控制方式
- 左键点击：触发宠物动作
- 右键点击：显示投喂菜单
- 拖动：移动宠物位置
- 系统托盘：右键退出
"""
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)
    
    print("✅ README已创建")

def main():
    """主函数"""
    print("=" * 50)
    print("桌面宠物程序 - 照片处理")
    print("=" * 50)
    
    # 输入照片路径
    input_photo = "/home/agentuser/.hermes/image_cache/img_55085c4e3197.jpg"
    
    if not os.path.exists(input_photo):
        print(f"❌ 错误: 照片不存在 {input_photo}")
        print("将使用默认宠物形象")
        return
    
    # 创建输出目录
    os.makedirs("assets/images", exist_ok=True)
    
    # 卡通化处理
    cartoon_output = "assets/images/cartoon_pet.png"
    
    if simple_cartoonize_pil(input_photo, cartoon_output):
        print("\n✅ 照片处理成功!")
        
        # 创建宠物状态图像
        if create_simple_pet_images(cartoon_output):
            # 创建食物图像
            create_food_images()
            
            # 更新配置
            update_main_program()
            
            print("\n" + "=" * 50)
            print("🎉 所有处理完成!")
            print("=" * 50)
            print("\n现在可以运行宠物程序了:")
            print("1. 安装PyQt5: pip install PyQt5")
            print("2. 启动程序: python src/main.py")
            print("\n或者直接运行: ./run.sh")
            
        else:
            print("\n⚠️ 创建状态图像失败，将使用默认形象")
            
    else:
        print("\n⚠️ 照片处理失败，将使用默认宠物形象")

if __name__ == "__main__":
    main()