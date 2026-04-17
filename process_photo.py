#!/usr/bin/env python3
"""
照片卡通化测试程序
"""

import cv2
import numpy as np
from PIL import Image
import os

def simple_cartoonize(input_path, output_path, size=(256, 256)):
    """
    简化的卡通化算法
    """
    print(f"处理照片: {input_path}")
    
    # 读取图像
    img = cv2.imread(input_path)
    if img is None:
        print(f"错误: 无法读取图像 {input_path}")
        return False
    
    print(f"原始尺寸: {img.shape}")
    
    # 调整大小
    img = cv2.resize(img, size)
    
    # 转换为RGB（OpenCV使用BGR）
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # 方法1: 简化的卡通效果
    try:
        # 1. 边缘检测
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(gray, 255,
                                     cv2.ADAPTIVE_THRESH_MEAN_C,
                                     cv2.THRESH_BINARY, 9, 9)
        
        # 2. 颜色量化（减少颜色数量）
        # 使用双边滤波平滑颜色
        color = cv2.bilateralFilter(img, 9, 75, 75)
        
        # 3. 减少颜色数量
        Z = color.reshape((-1, 3))
        Z = np.float32(Z)
        
        # 定义K-Means参数
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        K = 8  # 颜色数量
        _, labels, centers = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        
        # 转换回uint8
        centers = np.uint8(centers)
        res = centers[labels.flatten()]
        color_quantized = res.reshape((color.shape))
        
        # 4. 合并边缘和颜色
        cartoon = cv2.bitwise_and(color_quantized, color_quantized, mask=edges)
        
        # 保存结果
        cv2.imwrite(output_path, cartoon)
        
        print(f"卡通化完成: {output_path}")
        
        # 显示对比
        print("\n对比:")
        print(f"  原始: {os.path.getsize(input_path) / 1024:.1f} KB")
        print(f"  卡通: {os.path.getsize(output_path) / 1024:.1f} KB")
        
        return True
        
    except Exception as e:
        print(f"卡通化失败: {e}")
        
        # 备用方案：简单的颜色简化
        try:
            # 转换为PIL图像
            pil_img = Image.fromarray(img_rgb)
            
            # 减少颜色数量
            pil_img = pil_img.convert('P', palette=Image.ADAPTIVE, colors=16)
            
            # 保存
            pil_img.save(output_path)
            print(f"使用备用方案完成: {output_path}")
            return True
            
        except Exception as e2:
            print(f"备用方案也失败: {e2}")
            return False

def create_pet_variations(cartoon_path):
    """
    创建宠物的不同状态图像
    """
    print("\n创建宠物状态图像...")
    
    # 读取卡通图像
    img = cv2.imread(cartoon_path)
    if img is None:
        print("错误: 无法读取卡通图像")
        return
    
    # 创建不同状态的图像
    states = {
        "standing": img,  # 站立（原图）
        "crouching": None,  # 蹲下
        "sleeping": None   # 睡眠
    }
    
    # 创建蹲下状态（缩小并调整）
    h, w = img.shape[:2]
    crouching = cv2.resize(img, (w, int(h * 0.8)))
    
    # 添加蹲下效果（稍微变形）
    rows, cols = crouching.shape[:2]
    
    # 创建蹲下的透视效果
    pts1 = np.float32([[0,0], [cols-1,0], [0,rows-1], [cols-1,rows-1]])
    pts2 = np.float32([[0,0], [cols-1,0], [cols*0.1,rows-1], [cols*0.9,rows-1]])
    M = cv2.getPerspectiveTransform(pts1, pts2)
    crouching = cv2.warpPerspective(crouching, M, (cols, rows))
    
    states["crouching"] = crouching
    
    # 创建睡眠状态（水平放置）
    sleeping = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    sleeping = cv2.resize(sleeping, (int(h * 0.7), int(w * 0.7)))
    
    # 添加ZZZ文字
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(sleeping, 'Zzz', (10, 30), font, 0.8, (0, 0, 255), 2)
    
    states["sleeping"] = sleeping
    
    # 保存状态图像
    for state_name, state_img in states.items():
        if state_img is not None:
            output_path = f"assets/images/pet_{state_name}.png"
            cv2.imwrite(output_path, state_img)
            print(f"  已保存: {output_path}")
    
    return True

def main():
    """主函数"""
    print("=" * 50)
    print("照片卡通化处理程序")
    print("=" * 50)
    
    # 输入照片路径
    input_photo = "/home/agentuser/.hermes/image_cache/img_55085c4e3197.jpg"
    
    if not os.path.exists(input_photo):
        print(f"错误: 照片不存在 {input_photo}")
        return
    
    # 创建输出目录
    os.makedirs("assets/images", exist_ok=True)
    
    # 卡通化处理
    cartoon_output = "assets/images/cartoon_pet.png"
    
    if simple_cartoonize(input_photo, cartoon_output):
        print("\n✅ 卡通化成功!")
        
        # 创建不同状态
        create_pet_variations(cartoon_output)
        
        print("\n🎉 所有处理完成!")
        print(f"宠物图像已保存到: assets/images/")
        print("\n可以运行以下命令启动宠物程序:")
        print("  python src/main.py")
        
    else:
        print("\n❌ 卡通化失败，将使用默认宠物形象")

if __name__ == "__main__":
    main()