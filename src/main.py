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
                             QSystemTrayIcon, QMessageBox, QFileDialog,
                             QInputDialog, QLabel, QVBoxLayout, QPushButton,
                             QDialog, QHBoxLayout)
from PyQt5.QtCore import (Qt, QTimer, QPoint, QPropertyAnimation, 
                         QEasingCurve, QRect, pyqtProperty, QSize)
from PyQt5.QtGui import (QPainter, QPixmap, QColor, QPen, QBrush, 
                        QFont, QMovie, QIcon, QImage)
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
        self.animation_frame = 0
        self.action_animation = None
        self.food_animation = None
        
        # 加载配置
        self.config = self.load_config()
        
        # 检查是否需要选择照片
        if not self.config.get("user_photo_selected", False):
            self.show_photo_selection_dialog()
        
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
        # 优先使用卡通化后的用户照片
        cartoon_path = self.config.get("cartoon_path")
        if cartoon_path and os.path.exists(cartoon_path):
            try:
                self.pet_image = QPixmap(cartoon_path)
                if not self.pet_image.isNull():
                    self.pet_image = self.pet_image.scaled(
                        self.pet_size[0], self.pet_size[1],
                        Qt.KeepAspectRatio, Qt.SmoothTransformation
                    )
                    return
            except:
                pass
        
        # 使用默认头像
        default_path = "assets/images/default_avatar.png"
        if os.path.exists(default_path):
            try:
                self.pet_image = QPixmap(default_path)
                if not self.pet_image.isNull():
                    self.pet_image = self.pet_image.scaled(
                        self.pet_size[0], self.pet_size[1],
                        Qt.KeepAspectRatio, Qt.SmoothTransformation
                    )
                    return
            except:
                pass
        
        # 绘制临时宠物（圆形）
        self.pet_image = QPixmap(self.pet_size[0], self.pet_size[1])
        self.pet_image.fill(Qt.transparent)
        
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
            
        # 更换照片
        change_photo_action = QAction("更换照片", self)
        change_photo_action.triggered.connect(self.change_photo)
        tray_menu.addAction(change_photo_action)
        
        # 查看食物历史
        history_action = QAction("查看食物历史", self)
        history_action.triggered.connect(self.show_food_history)
        tray_menu.addAction(history_action)
        
        tray_menu.addSeparator()
        
        # 退出动作
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(self.quit_application)
        tray_menu.addAction(exit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        
    def quit_application(self):
        """退出应用程序"""
        self.save_config()
        QApplication.quit()
        
    def change_photo(self):
        """更换照片"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择新照片", "", 
            "图片文件 (*.jpg *.jpeg *.png *.bmp *.gif)"
        )
        
        if file_path:
            cartoon_path = "assets/images/user_pet.png"
            if cartoonize_photo(file_path, cartoon_path):
                self.config["user_photo"] = file_path
                self.config["cartoon_path"] = cartoon_path
                self.config["use_default_avatar"] = False
                self.save_config()
                
                # 重新加载宠物图像
                self.load_pet_image()
                self.update()
                QMessageBox.information(self, "成功", "照片更换成功！")
            else:
                QMessageBox.warning(self, "错误", "照片处理失败")
    
    def show_food_history(self):
        """显示食物历史"""
        history = self.config.get("food_history", [])
        if not history:
            QMessageBox.information(self, "食物历史", "还没有投喂记录")
            return
        
        history_text = "食物投喂记录:\n\n"
        for item in history[-10:]:  # 显示最近10条
            history_text += f"{item['time']} - {item['food']}\n"
        
        QMessageBox.information(self, "食物历史", history_text)
        self.start_feed_animation(food)
        
        # 记录食物历史
        if "food_history" not in self.config:
            self.config["food_history"] = []
        self.config["food_history"].append({
            "food": food,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        self.save_config()
    
    def start_feed_animation(self, food):
        """开始投喂动画"""
        self.food_animation = food
        self.food_frame = 0
        
        # 加载食物图像
        food_images = {
            "汉堡": "assets/images/hamburger.png",
            "炸鸡": "assets/images/fried_chicken.png",
            "螺蛳粉": "assets/images/luosifen.png"
        }
        
        food_path = food_images.get(food)
        if food_path and os.path.exists(food_path):
            self.food_image = QPixmap(food_path)
            self.food_image = self.food_image.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        else:
            # 创建默认食物图像
            self.food_image = QPixmap(50, 50)
            self.food_image.fill(Qt.transparent)
            painter = QPainter(self.food_image)
            painter.setBrush(QBrush(QColor(255, 200, 100)))
            painter.drawEllipse(5, 5, 40, 40)
            painter.end()
        
        # 开始动画定时器
        self.feed_timer = QTimer()
        self.feed_timer.timeout.connect(self.update_feed_frame)
        self.feed_timer.start(50)  # 20fps
    
    def update_feed_frame(self):
        """更新投喂帧"""
        self.food_frame += 1
        if self.food_frame > 40:  # 2秒动画
            self.feed_timer.stop()
            self.food_animation = None
            self.update()
            return
        
        # 在绘制事件中显示食物动画
        self.update()
    
    def paintEvent(self, event):
        """绘制事件"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 绘制宠物图像
        painter.drawPixmap(0, 0, self.pet_image)
        
        # 绘制投喂动画
        if self.food_animation and hasattr(self, 'food_image'):
            # 食物从上方落下的动画
            food_y = -50 + self.food_frame * 3  # 从上方落下
            if food_y < 100:  # 在宠物上方
                food_x = 50  # 居中
                painter.drawPixmap(food_x, food_y, self.food_image)
            
            # 绘制食物名称
            if self.food_frame > 20:  # 后半段显示文字
                painter.setFont(QFont("Arial", 10))
                painter.setPen(QColor(255, 100, 100))
                painter.drawText(60, 120, self.food_animation)
        
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
        
        # 开始动作动画
        self.start_action_animation(self.current_action)
        
        print(f"触发动作: {self.current_action}")
    
    def start_action_animation(self, action):
        """开始动作动画"""
        self.action_animation = action
        self.animation_frame = 0
        
        # 根据动作设置动画参数
        if action == "wave":
            self.wave_animation()
        elif action == "jump":
            self.jump_animation()
        elif action == "walk":
            self.walk_animation()
    
    def wave_animation(self):
        """挥手动画"""
        # 保存原始图像
        self.original_image = self.pet_image.copy()
        
        # 创建动画定时器
        self.wave_timer = QTimer()
        self.wave_timer.timeout.connect(self.update_wave_frame)
        self.wave_timer.start(100)  # 10fps
        self.wave_frame = 0
    
    def update_wave_frame(self):
        """更新挥手帧"""
        self.wave_frame += 1
        if self.wave_frame > 10:  # 1秒动画
            self.wave_timer.stop()
            self.pet_image = self.original_image
            self.action_animation = None
            self.update()
            return
        
        # 创建挥手效果的图像
        temp_image = self.original_image.copy()
        painter = QPainter(temp_image)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 根据帧数绘制挥手效果
        wave_height = 10 * abs(5 - self.wave_frame) / 5  # 中间最高
        
        # 绘制挥手线
        painter.setPen(QPen(QColor(255, 100, 100), 3))
        painter.drawLine(120, 60, 140, 60 - wave_height)
        
        painter.end()
        self.pet_image = temp_image
        self.update()
    
    def jump_animation(self):
        """跳跃动画"""
        self.jump_timer = QTimer()
        self.jump_timer.timeout.connect(self.update_jump_frame)
        self.jump_timer.start(50)  # 20fps
        self.jump_frame = 0
        self.original_pos = self.pos()
    
    def update_jump_frame(self):
        """更新跳跃帧"""
        self.jump_frame += 1
        if self.jump_frame > 20:  # 1秒动画
            self.jump_timer.stop()
            self.move(self.original_pos)
            self.action_animation = None
            return
        
        # 跳跃轨迹：正弦波
        height = 30 * abs(10 - self.jump_frame) / 10  # 中间最高
        new_pos = QPoint(self.original_pos.x(), self.original_pos.y() - int(height))
        self.move(new_pos)
    
    def walk_animation(self):
        """踱步动画"""
        self.walk_timer = QTimer()
        self.walk_timer.timeout.connect(self.update_walk_frame)
        self.walk_timer.start(200)  # 5fps
        self.walk_frame = 0
        self.walk_direction = 1  # 1向右，-1向左
    
    def update_walk_frame(self):
        """更新踱步帧"""
        self.walk_frame += 1
        if self.walk_frame > 10:  # 2秒动画
            self.walk_timer.stop()
            self.action_animation = None
            return
        
        # 左右移动
        move_distance = 5 * self.walk_direction
        new_pos = QPoint(self.x() + move_distance, self.y())
        
        # 检查边界
        screen_geometry = QApplication.desktop().availableGeometry()
        if new_pos.x() < 0 or new_pos.x() > screen_geometry.width() - self.width():
            self.walk_direction *= -1  # 反向
            new_pos = QPoint(self.x() - move_distance, self.y())
        
        self.move(new_pos)
        
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
            "food_history": [],
            "user_photo_selected": False,
            "use_default_avatar": False,
            "user_photo": None,
            "cartoon_path": None
        }
        
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # 合并配置，确保新字段存在
                    for key in default_config:
                        if key not in loaded_config:
                            loaded_config[key] = default_config[key]
                    return loaded_config
            except:
                return default_config
        return default_config
        
    def save_config(self):
        """保存配置文件"""
        config = {
            "pet_size": [self.width(), self.height()],
            "position": [self.x(), self.y()],
            "last_state": self.current_state,
            "food_history": [],  # TODO: 添加食物历史
            "user_photo_selected": self.config.get("user_photo_selected", False),
            "use_default_avatar": self.config.get("use_default_avatar", False),
            "user_photo": self.config.get("user_photo"),
            "cartoon_path": self.config.get("cartoon_path")
        }
        
        os.makedirs("config", exist_ok=True)
        with open("config/pet_config.json", 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
            
    def show_photo_selection_dialog(self):
        """显示照片选择对话框"""
        dialog = QDialog(self)
        dialog.setWindowTitle("选择照片创建宠物")
        dialog.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        
        # 标题
        title_label = QLabel("欢迎使用桌面宠物！")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # 说明
        desc_label = QLabel("请选择一张照片，系统将为您生成动漫风格的宠物")
        desc_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc_label)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        
        # 选择照片按钮
        select_btn = QPushButton("选择照片")
        select_btn.clicked.connect(lambda: self.select_photo(dialog))
        button_layout.addWidget(select_btn)
        
        # 使用默认头像按钮
        default_btn = QPushButton("使用默认头像")
        default_btn.clicked.connect(lambda: self.use_default_avatar(dialog))
        button_layout.addWidget(default_btn)
        
        layout.addLayout(button_layout)
        
        # 跳过按钮
        skip_btn = QPushButton("稍后选择")
        skip_btn.clicked.connect(dialog.accept)
        layout.addWidget(skip_btn)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def select_photo(self, dialog):
        """选择照片"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择照片", "", 
            "图片文件 (*.jpg *.jpeg *.png *.bmp *.gif)"
        )
        
        if file_path:
            # 保存照片路径
            self.photo_path = file_path
            self.config["user_photo"] = file_path
            self.config["user_photo_selected"] = True
            
            # 卡通化处理
            cartoon_path = "assets/images/user_pet.png"
            if cartoonize_photo(file_path, cartoon_path):
                self.config["cartoon_path"] = cartoon_path
                QMessageBox.information(self, "成功", "宠物创建成功！")
            else:
                QMessageBox.warning(self, "警告", "照片处理失败，使用默认头像")
                self.use_default_avatar(dialog, show_message=False)
            
            self.save_config()
            dialog.accept()
    
    def use_default_avatar(self, dialog, show_message=True):
        """使用默认头像"""
        self.config["user_photo_selected"] = True
        self.config["use_default_avatar"] = True
        self.save_config()
        
        if show_message:
            QMessageBox.information(self, "提示", "已使用默认头像，您可以在设置中更改")
        
        dialog.accept()
        
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