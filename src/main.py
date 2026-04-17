#!/usr/bin/env python3
"""
桌面宠物程序 - 主程序
基于用户照片生成动漫风格桌面宠物
"""

import sys
import os
import json
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (QApplication, QWidget, QMenu, QAction, 
                             QSystemTrayIcon, QMessageBox)
from PyQt5.QtCore import (Qt, QTimer, QPoint, QPropertyAnimation, 
                         QEasingCurve, QRect, pyqtProperty)
from PyQt5.QtGui import (QPainter, QPixmap, QColor, QPen, QBrush, 
                        QFont, QMovie, QIcon)
import numpy as np
import cv2
from PIL import Image

class DesktopPet(QWidget):
    """桌面宠物主窗口类"""
    
    def __init__(self, photo_path=None):
        super().__init__()
        
        # 初始化变量
        self.photo_path = photo_path
        self.pet_size = (150, 150)  # 宠物尺寸
        self.is_dragging = False
        self.drag_position = QPoint()
        self.last_interaction = datetime.now()
        self.current_state = "standing"  # standing, crouching, sleeping
        self.current_action = None
        self.food_list = ["汉堡", "炸鸡", "螺蛳粉"]
        
        # 加载配置
        self.config = self.load_config()
        
        # 初始化UI
        self.init_ui()
        
        # 初始化动画定时器
        self.init_timers()
        
        # 初始化系统托盘
        self.init_tray()
        
    def init_ui(self):
        """初始化用户界面"""
        # 设置窗口属性
        self.setWindowFlags(
            Qt.FramelessWindowHint |  # 无边框
            Qt.WindowStaysOnTopHint |  # 始终在最前
            Qt.Tool  # 不显示在任务栏
        )
        
        # 设置窗口透明
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # 设置窗口大小和位置
        self.resize(*self.pet_size)
        screen_geometry = QApplication.desktop().availableGeometry()
        self.move(
            screen_geometry.width() - self.pet_size[0] - 20,
            screen_geometry.height() - self.pet_size[1] - 20
        )
        
        # 设置鼠标跟踪
        self.setMouseTracking(True)
        
        # 加载宠物图像
        self.load_pet_image()
        
    def load_pet_image(self):
        """加载宠物图像"""
        # 临时使用占位图像
        self.pet_image = QPixmap(self.pet_size[0], self.pet_size[1])
        self.pet_image.fill(Qt.transparent)
        
        # 绘制临时宠物（圆形）
        painter = QPainter(self.pet_image)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 绘制身体（蓝色圆形）
        painter.setBrush(QBrush(QColor(100, 150, 255, 200)))
        painter.setPen(QPen(QColor(50, 100, 200), 2))
        painter.drawEllipse(10, 10, 130, 130)
        
        # 绘制眼睛
        painter.setBrush(QBrush(Qt.white))
        painter.drawEllipse(40, 40, 20, 20)
        painter.drawEllipse(90, 40, 20, 20)
        
        painter.setBrush(QBrush(Qt.black))
        painter.drawEllipse(45, 45, 10, 10)
        painter.drawEllipse(95, 45, 10, 10)
        
        # 绘制嘴巴
        painter.setPen(QPen(Qt.black, 3))
        painter.drawArc(50, 80, 50, 30, 0, 180 * 16)
        
        painter.end()
        
        # TODO: 后续替换为卡通化后的用户照片
        
    def init_timers(self):
        """初始化定时器"""
        # 动画更新定时器（30fps）
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_timer.start(33)  # 约30fps
        
        # 状态检查定时器（每5秒检查一次）
        self.state_timer = QTimer()
        self.state_timer.timeout.connect(self.check_state)
        self.state_timer.start(5000)
        
    def init_tray(self):
        """初始化系统托盘"""
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(self.pet_image))
        
        # 创建托盘菜单
        tray_menu = QMenu()
        
        # 投喂动作
        feed_menu = tray_menu.addMenu("投喂")
        for food in self.food_list:
            action = QAction(food, self)
            action.triggered.connect(lambda checked, f=food: self.feed_pet(f))
            feed_menu.addAction(action)
            
        # 退出动作
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(self.quit_application)
        tray_menu.addAction(exit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        
    def paintEvent(self, event):
        """绘制事件"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 绘制宠物图像
        painter.drawPixmap(0, 0, self.pet_image)
        
        # 根据状态添加效果
        if self.current_state == "sleeping":
            # 添加睡眠效果（ZZZ）
            painter.setFont(QFont("Arial", 12))
            painter.setPen(Qt.blue)
            painter.drawText(60, 30, "Zzz")
            
    def mousePressEvent(self, event):
        """鼠标按下事件"""
        if event.button() == Qt.LeftButton:
            # 左键点击：触发动作
            self.trigger_action()
            self.last_interaction = datetime.now()
            
        elif event.button() == Qt.RightButton:
            # 右键：显示投喂菜单
            self.show_feed_menu(event.globalPos())
            
        # 开始拖动
        self.is_dragging = True
        self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
        event.accept()
        
    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        if self.is_dragging and event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()
            
    def mouseReleaseEvent(self, event):
        """鼠标释放事件"""
        self.is_dragging = False
        
    def trigger_action(self):
        """触发宠物动作"""
        actions = ["wave", "jump", "walk"]
        import random
        self.current_action = random.choice(actions)
        
        # 更新最后交互时间
        self.last_interaction = datetime.now()
        
        # 重置状态为站立
        self.current_state = "standing"
        
        # TODO: 实现具体动作动画
        
    def show_feed_menu(self, position):
        """显示投喂菜单"""
        menu = QMenu(self)
        
        for food in self.food_list:
            action = QAction(food, self)
            action.triggered.connect(lambda checked, f=food: self.feed_pet(f))
            menu.addAction(action)
            
        menu.exec_(position)
        
    def feed_pet(self, food):
        """投喂宠物"""
        print(f"投喂: {food}")
        self.last_interaction = datetime.now()
        self.current_state = "standing"
        
        # TODO: 实现投喂动画
        
    def check_state(self):
        """检查并更新宠物状态"""
        now = datetime.now()
        idle_time = (now - self.last_interaction).total_seconds()
        
        if idle_time > 60:  # 1分钟无交互
            self.current_state = "crouching"
        if idle_time > 120:  # 2分钟无交互
            self.current_state = "sleeping"
            
    def update_animation(self):
        """更新动画"""
        self.update()  # 触发重绘
        
    def load_config(self):
        """加载配置文件"""
        config_path = "config/pet_config.json"
        default_config = {
            "pet_size": [150, 150],
            "position": [100, 100],
            "last_state": "standing",
            "food_history": []
        }
        
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return default_config
        return default_config
        
    def save_config(self):
        """保存配置文件"""
        config = {
            "pet_size": [self.width(), self.height()],
            "position": [self.x(), self.y()],
            "last_state": self.current_state,
            "food_history": []  # TODO: 添加食物历史
        }
        
        os.makedirs("config", exist_ok=True)
        with open("config/pet_config.json", 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
            
    def quit_application(self):
        """退出应用程序"""
        self.save_config()
        QApplication.quit()
        
    def closeEvent(self, event):
        """关闭事件"""
        self.save_config()
        event.accept()

def cartoonize_photo(photo_path, output_path):
    """
    将照片转换为动漫风格
    使用简化的卡通化算法（后续可替换为AnimeGAN）
    """
    try:
        # 读取图像
        img = cv2.imread(photo_path)
        if img is None:
            print(f"无法读取图像: {photo_path}")
            return None
            
        # 调整大小
        img = cv2.resize(img, (256, 256))
        
        # 简化的卡通化效果
        # 1. 边缘检测
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(gray, 255,
                                     cv2.ADAPTIVE_THRESH_MEAN_C,
                                     cv2.THRESH_BINARY, 9, 9)
        
        # 2. 颜色量化
        color = cv2.bilateralFilter(img, 9, 300, 300)
        
        # 3. 合并边缘和颜色
        cartoon = cv2.bitwise_and(color, color, mask=edges)
        
        # 保存结果
        cv2.imwrite(output_path, cartoon)
        print(f"卡通化完成: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"卡通化失败: {e}")
        return None

def main():
    """主函数"""
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    # 检查照片路径
    photo_path = None
    if len(sys.argv) > 1:
        photo_path = sys.argv[1]
    
    # 如果提供了照片，先进行卡通化
    if photo_path and os.path.exists(photo_path):
        print(f"处理照片: {photo_path}")
        cartoon_path = "assets/images/cartoon_pet.png"
        cartoonize_photo(photo_path, cartoon_path)
    
    # 创建宠物窗口
    pet = DesktopPet(photo_path)
    pet.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()