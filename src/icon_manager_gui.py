#!/usr/bin/env python3
"""
桌面宠物 - 快捷方式图标管理器
允许用户自定义桌面快捷方式图标
"""

import os
import sys
import json
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QListWidget, QListWidgetItem,
                             QFileDialog, QMessageBox, QDialog)
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, QSize

class IconManagerDialog(QDialog):
    """图标管理器对话框"""
    
    def __init__(self, install_dir=None):
        super().__init__()
        self.install_dir = install_dir or os.path.dirname(os.path.abspath(__file__))
        self.icon_dir = os.path.join(self.install_dir, "assets", "icons")
        self.user_icon_dir = os.path.join(self.install_dir, "user_icons")
        
        # 创建目录
        os.makedirs(self.icon_dir, exist_ok=True)
        os.makedirs(self.user_icon_dir, exist_ok=True)
        
        self.init_ui()
        self.load_icons()
        
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("桌面宠物 - 图标管理器")
        self.setFixedSize(600, 500)
        
        layout = QVBoxLayout()
        
        # 标题
        title_label = QLabel("自定义桌面快捷方式图标")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # 说明
        desc_label = QLabel("支持的图标格式: .ico, .png, .jpg, .bmp\n图标大小建议: 256x256 或 128x128")
        desc_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc_label)
        
        # 图标列表
        self.icon_list = QListWidget()
        self.icon_list.setIconSize(QSize(64, 64))
        self.icon_list.itemDoubleClicked.connect(self.select_icon)
        layout.addWidget(self.icon_list)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        
        # 添加图标按钮
        add_btn = QPushButton("添加图标")
        add_btn.clicked.connect(self.add_icon)
        button_layout.addWidget(add_btn)
        
        # 选择按钮
        select_btn = QPushButton("选择此图标")
        select_btn.clicked.connect(self.select_current_icon)
        button_layout.addWidget(select_btn)
        
        # 删除按钮
        delete_btn = QPushButton("删除图标")
        delete_btn.clicked.connect(self.delete_icon)
        button_layout.addWidget(delete_btn)
        
        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(self.close)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
        # 当前图标信息
        self.current_icon_label = QLabel("当前图标: 默认图标")
        self.current_icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.current_icon_label)
        
        self.setLayout(layout)
        
        # 加载当前配置
        self.load_current_config()
    
    def load_icons(self):
        """加载所有图标"""
        self.icon_list.clear()
        
        # 系统图标
        system_icons = self.get_icons_in_dir(self.icon_dir, "系统图标")
        for icon in system_icons:
            self.add_icon_to_list(icon["path"], icon["name"], "system")
        
        # 用户图标
        user_icons = self.get_icons_in_dir(self.user_icon_dir, "用户图标")
        for icon in user_icons:
            self.add_icon_to_list(icon["path"], icon["name"], "user")
    
    def get_icons_in_dir(self, directory, category):
        """获取目录中的图标文件"""
        icons = []
        if os.path.exists(directory):
            for file in os.listdir(directory):
                if file.lower().endswith(('.ico', '.png', '.jpg', '.jpeg', '.bmp')):
                    icons.append({
                        "path": os.path.join(directory, file),
                        "name": file,
                        "category": category
                    })
        return icons
    
    def add_icon_to_list(self, icon_path, icon_name, icon_type):
        """添加图标到列表"""
        try:
            icon = QIcon(icon_path)
            if not icon.isNull():
                item = QListWidgetItem(icon, icon_name)
                item.setData(Qt.UserRole, {
                    "path": icon_path,
                    "type": icon_type
                })
                self.icon_list.addItem(item)
        except:
            pass
    
    def add_icon(self):
        """添加新图标"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择图标文件", "",
            "图标文件 (*.ico *.png *.jpg *.jpeg *.bmp)"
        )
        
        if file_path:
            # 复制到用户图标目录
            import shutil
            import uuid
            filename = os.path.basename(file_path)
            dest_path = os.path.join(self.user_icon_dir, filename)
            
            # 如果文件名已存在，添加随机后缀
            if os.path.exists(dest_path):
                name, ext = os.path.splitext(filename)
                filename = f"{name}_{uuid.uuid4().hex[:4]}{ext}"
                dest_path = os.path.join(self.user_icon_dir, filename)
            
            try:
                shutil.copy2(file_path, dest_path)
                self.add_icon_to_list(dest_path, filename, "user")
                QMessageBox.information(self, "成功", "图标添加成功！")
            except Exception as e:
                QMessageBox.warning(self, "错误", f"添加图标失败: {e}")
    
    def select_current_icon(self):
        """选择当前选中的图标"""
        current_item = self.icon_list.currentItem()
        if current_item:
            icon_data = current_item.data(Qt.UserRole)
            self.set_current_icon(icon_data["path"])
    
    def select_icon(self, item):
        """双击选择图标"""
        icon_data = item.data(Qt.UserRole)
        self.set_current_icon(icon_data["path"])
    
    def delete_icon(self):
        """删除选中的图标"""
        current_item = self.icon_list.currentItem()
        if current_item:
            icon_data = current_item.data(Qt.UserRole)
            if icon_data["type"] == "user":  # 只能删除用户图标
                reply = QMessageBox.question(
                    self, "确认删除",
                    f"确定要删除图标 '{current_item.text()}' 吗？",
                    QMessageBox.Yes | QMessageBox.No
                )
                
                if reply == QMessageBox.Yes:
                    try:
                        os.remove(icon_data["path"])
                        self.icon_list.takeItem(self.icon_list.row(current_item))
                        QMessageBox.information(self, "成功", "图标已删除")
                    except Exception as e:
                        QMessageBox.warning(self, "错误", f"删除失败: {e}")
            else:
                QMessageBox.warning(self, "提示", "系统图标不能删除")
    
    def load_current_config(self):
        """加载当前配置"""
        config_path = os.path.join(self.install_dir, "config", "shortcut_config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    current_icon = config.get("current_icon")
                    if current_icon and os.path.exists(current_icon):
                        self.current_icon_label.setText(f"当前图标: {os.path.basename(current_icon)}")
            except:
                pass
    
    def set_current_icon(self, icon_path):
        """设置当前图标"""
        if not os.path.exists(icon_path):
            QMessageBox.warning(self, "错误", "图标文件不存在")
            return
        
        # 保存配置
        config_path = os.path.join(self.install_dir, "config", "shortcut_config.json")
        config = {
            "current_icon": icon_path,
            "last_updated": os.path.getmtime(icon_path)
        }
        
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        # 更新显示
        self.current_icon_label.setText(f"当前图标: {os.path.basename(icon_path)}")
        
        # 创建快捷方式
        self.create_shortcut(icon_path)
        
        QMessageBox.information(self, "成功", "图标设置成功！桌面快捷方式已更新。")
    
    def create_shortcut(self, icon_path):
        """创建桌面快捷方式"""
        try:
            import win32com.client
            import pythoncom
            
            # 获取桌面路径
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            shortcut_path = os.path.join(desktop, "DesktopPet.lnk")
            
            # 目标路径
            target_path = os.path.join(self.install_dir, "run.bat")
            
            # 创建快捷方式
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.TargetPath = target_path
            shortcut.WorkingDirectory = self.install_dir
            shortcut.IconLocation = icon_path
            shortcut.save()
            
            return True
        except Exception as e:
            print(f"创建快捷方式失败: {e}")
            
            # 使用VBScript作为备选方案
            try:
                vbs_script = f"""
Set WshShell = CreateObject("WScript.Shell")
Set oShellLink = WshShell.CreateShortcut("{desktop}\\DesktopPet.lnk")
oShellLink.TargetPath = "{target_path}"
oShellLink.WorkingDirectory = "{self.install_dir}"
oShellLink.IconLocation = "{icon_path}"
oShellLink.Save
"""
                
                vbs_path = os.path.join(self.install_dir, "create_shortcut.vbs")
                with open(vbs_path, 'w', encoding='utf-8') as f:
                    f.write(vbs_script)
                
                import subprocess
                subprocess.run(['cscript', '//nologo', vbs_path], shell=True)
                os.remove(vbs_path)
                
                return True
            except Exception as e2:
                print(f"备选方案也失败: {e2}")
                return False

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 获取安装目录
    if len(sys.argv) > 1:
        install_dir = sys.argv[1]
    else:
        install_dir = os.path.dirname(os.path.abspath(__file__))
    
    dialog = IconManagerDialog(install_dir)
    dialog.exec_()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()