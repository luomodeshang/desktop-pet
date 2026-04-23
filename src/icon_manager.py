#!/usr/bin/env python3
"""
桌面宠物程序 - 图标管理器
处理快捷方式图标和用户自定义图标
"""

import os
import sys
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize

class IconManager:
    """图标管理器"""
    
    def __init__(self, install_dir=None):
        self.install_dir = install_dir or os.path.dirname(os.path.abspath(__file__))
        self.icon_dir = os.path.join(self.install_dir, "assets", "icons")
        self.user_icon_dir = os.path.join(self.install_dir, "user_icons")
        
        # 创建目录
        os.makedirs(self.icon_dir, exist_ok=True)
        os.makedirs(self.user_icon_dir, exist_ok=True)
        
    def get_available_icons(self):
        """获取可用的图标文件"""
        icon_extensions = ['.ico', '.png', '.jpg', '.jpeg', '.bmp']
        icons = []
        
        # 检查系统图标目录
        if os.path.exists(self.icon_dir):
            for file in os.listdir(self.icon_dir):
                if any(file.lower().endswith(ext) for ext in icon_extensions):
                    icons.append({
                        'path': os.path.join(self.icon_dir, file),
                        'name': file,
                        'type': 'system'
                    })
        
        # 检查用户图标目录
        if os.path.exists(self.user_icon_dir):
            for file in os.listdir(self.user_icon_dir):
                if any(file.lower().endswith(ext) for ext in icon_extensions):
                    icons.append({
                        'path': os.path.join(self.user_icon_dir, file),
                        'name': file,
                        'type': 'user'
                    })
        
        return icons
    
    def load_icon(self, icon_path=None, size=64):
        """加载图标"""
        if icon_path and os.path.exists(icon_path):
            try:
                icon = QIcon(icon_path)
                if not icon.isNull():
                    return icon
            except:
                pass
        
        # 使用默认图标
        default_icon = os.path.join(self.install_dir, "assets", "images", "icon.ico")
        if os.path.exists(default_icon):
            return QIcon(default_icon)
        
        # 创建默认图标
        return self.create_default_icon()
    
    def create_default_icon(self):
        """创建默认图标"""
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.transparent)
        
        # 这里可以绘制一个简单的图标
        # 暂时返回空图标
        return QIcon(pixmap)
    
    def save_user_icon(self, source_path):
        """保存用户上传的图标"""
        if not os.path.exists(source_path):
            return None
        
        # 生成唯一文件名
        import uuid
        ext = os.path.splitext(source_path)[1].lower()
        if ext not in ['.ico', '.png', '.jpg', '.jpeg', '.bmp']:
            ext = '.png'
        
        filename = f"user_icon_{uuid.uuid4().hex[:8]}{ext}"
        dest_path = os.path.join(self.user_icon_dir, filename)
        
        try:
            # 如果是图片文件，可以调整大小
            from PIL import Image
            img = Image.open(source_path)
            img = img.resize((256, 256), Image.Resampling.LANCZOS)
            
            # 转换为ICO格式（如果需要）
            if ext == '.ico':
                img.save(dest_path, format='ICO')
            else:
                img.save(dest_path)
            
            return dest_path
        except Exception as e:
            print(f"保存图标失败: {e}")
            # 直接复制文件
            import shutil
            shutil.copy2(source_path, dest_path)
            return dest_path
    
    def create_shortcut_icon(self, icon_path=None):
        """创建快捷方式图标文件"""
        if icon_path and os.path.exists(icon_path):
            return icon_path
        
        # 使用默认图标
        default_icon = os.path.join(self.install_dir, "assets", "images", "icon.ico")
        if os.path.exists(default_icon):
            return default_icon
        
        # 创建默认ICO文件
        default_icon_path = os.path.join(self.icon_dir, "default.ico")
        if not os.path.exists(default_icon_path):
            self.create_ico_file(default_icon_path)
        
        return default_icon_path
    
    def create_ico_file(self, output_path):
        """创建ICO文件"""
        try:
            from PIL import Image, ImageDraw
            
            # 创建256x256的图标
            img = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # 绘制圆形宠物图标
            draw.ellipse([50, 50, 206, 206], fill=(100, 150, 255, 200))
            draw.ellipse([90, 90, 120, 120], fill=(255, 255, 255, 255))  # 左眼
            draw.ellipse([136, 90, 166, 120], fill=(255, 255, 255, 255))  # 右眼
            draw.ellipse([100, 100, 110, 110], fill=(0, 0, 0, 255))  # 左眼珠
            draw.ellipse([146, 100, 156, 110], fill=(0, 0, 0, 255))  # 右眼珠
            
            # 绘制微笑嘴巴
            draw.arc([100, 140, 156, 180], 0, 180, fill=(0, 0, 0, 255), width=5)
            
            # 保存为ICO
            img.save(output_path, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
            return True
        except Exception as e:
            print(f"创建ICO文件失败: {e}")
            return False

if __name__ == "__main__":
    # 测试代码
    manager = IconManager()
    icons = manager.get_available_icons()
    print(f"找到 {len(icons)} 个图标:")
    for icon in icons:
        print(f"  - {icon['name']} ({icon['type']})")