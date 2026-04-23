#!/usr/bin/env python3
"""
桌面宠物程序 - 主程序
基于用户照片生成动漫风格桌面宠物
"""

import sys
import os
import json
import random
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (QApplication, QWidget, QMenu, QAction, 
                             QSystemTrayIcon, QMessageBox, QFileDialog,
                             QLabel, QVBoxLayout, QPushButton, QDialog, QHBoxLayout)
from PyQt5.QtCore import (Qt, QTimer, QPoint, QRect)
from PyQt5.QtGui import (QPainter, QPixmap, QColor, QPen, QBrush, 
                        QFont, QIcon, QImage, QPainterPath)
import numpy as np
import cv2
from PIL import Image

def cartoonize_photo(input_path, output_path):
    """
    将照片卡通化处理
    """
    try:
        # 读取图像
        img = cv2.imread(input_path)
        if img is None:
            print(f"无法读取图片: {input_path}")
            return False
        
        # 缩放图像到合适大小
        img = cv2.resize(img, (256, 256))
        
        # 1. 中值滤波降噪
        img = cv2.medianBlur(img, 5)
        
        # 2. 边缘检测
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.adaptiveThreshold(gray, 255, 
                                      cv2.ADAPTIVE_THRESH_MEAN_C, 
                                      cv2.THRESH_BINARY, 9, 9)
        
        # 3. 双边滤波（保持边缘的平滑）
        color = cv2.bilateralFilter(img, 9, 300, 300)
        
        # 4. 卡通化效果
        cartoon = cv2.bitwise_and(color, color, mask=edges)
        
        # 5. 保存
        cv2.imwrite(output_path, cartoon)
        print(f"卡通化完成: {output_path}")
        return True
        
    except Exception as e:
        print(f"卡通化失败: {e}")
        return False


class DesktopPet(QWidget):
    """桌面宠物主窗口类"""
    
    def __init__(self, photo_path=None):
        super().__init__()
        
        # 初始化变量
        self.photo_path = photo_path
        self.pet_size = (150, 150)
        self.is_dragging = False
        self.drag_position = QPoint()
        self.last_interaction = datetime.now()
        self.current_state = "standing"
        self.current_action = None
        self.food_list = ["汉堡", "炸鸡", "螺蛳粉"]
        self.animation_frame = 0
        self.action_animation = None
        self.food_animation = None
        self.food_frame = 0
        self.food_image = None
        
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
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        
        # 设置窗口透明
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # 设置窗口大小和位置
        self.resize(*self.pet_size)
        screen_geometry = QApplication.desktop().availableGeometry()
        self.move(
            screen_geometry.width() - self.pet_size[0] - 40,
            screen_geometry.height() - self.pet_size[1] - 80
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
        
        path = QPainterPath()
        path.addEllipse(10, 10, 130, 130)
        painter.setClipPath(path)
        
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
        # 状态检查定时器（每5秒检查一次）
        self.state_timer = QTimer()
        self.state_timer.timeout.connect(self.check_state)
        self.state_timer.start(5000)
        
    def init_tray(self):
        """初始化系统托盘"""
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(self.pet_image))
        self.tray_icon.show()
        
        # 创建托盘菜单
        tray_menu = QMenu()
        
        # 投喂子菜单
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
        for item in history[-10:]:
            history_text += f"{item['time']} - {item['food']}\n"
        
        QMessageBox.information(self, "食物历史", history_text)
    
    def show_photo_selection_dialog(self):
        """显示照片选择对话框"""
        dialog = QDialog(self)
        dialog.setWindowTitle("选择照片创建宠物")
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        dialog.setFixedSize(400, 250)
        
        layout = QVBoxLayout()
        
        # 标题
        title_label = QLabel("欢迎使用桌面宠物！")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # 说明
        desc_label = QLabel("请选择一张照片，系统将为您生成卡通风格的宠物")
        desc_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc_label)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        
        # 选择照片按钮
        select_btn = QPushButton("📷 选择照片")
        select_btn.setMinimumHeight(40)
        select_btn.clicked.connect(lambda: self.select_photo(dialog))
        button_layout.addWidget(select_btn)
        
        # 使用默认头像按钮
        default_btn = QPushButton("😊 使用默认头像")
        default_btn.setMinimumHeight(40)
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
        """选择照片并卡通化"""
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
                self.config["use_default_avatar"] = False
                QMessageBox.information(None, "成功", "宠物创建成功！")
            else:
                QMessageBox.warning(None, "警告", "照片处理失败，已使用默认头像")
                self.config["use_default_avatar"] = True
            
            self.save_config()
            dialog.accept()
    
    def use_default_avatar(self, dialog, show_message=True):
        """使用默认头像"""
        self.config["user_photo_selected"] = True
        self.config["use_default_avatar"] = True
        self.save_config()
        
        if show_message:
            QMessageBox.information(None, "提示", "已使用默认头像，您可以在设置中更改")
        
        dialog.accept()
    
    # ====== 鼠标事件 ======
    
    def mousePressEvent(self, event):
        """鼠标按下事件"""
        if event.button() == Qt.LeftButton:
            # 左键点击：触发动作
            self.trigger_action()
            self.last_interaction = datetime.now()
            
            # 开始拖动（但保留动作触发）
            
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
    
    # ====== 动作系统 ======
    
    def trigger_action(self):
        """触发宠物动作"""
        actions = ["wave", "jump", "walk"]
        self.current_action = random.choice(actions)
        self.last_interaction = datetime.now()
        self.current_state = "standing"
        print(f"触发动作: {self.current_action}")
        
        if self.current_action == "wave":
            self.start_wave()
        elif self.current_action == "jump":
            self.start_jump()
        elif self.current_action == "walk":
            self.start_walk()
    
    def start_wave(self):
        """开始挥手动画"""
        self.action_animation = "wave"
        self.wave_frame = 0
        self.wave_timer = QTimer()
        self.wave_timer.timeout.connect(self.wave_update)
        self.wave_timer.start(80)
    
    def wave_update(self):
        """挥手动画更新"""
        self.wave_frame += 1
        if self.wave_frame > 12:
            self.wave_timer.stop()
            self.wave_timer.deleteLater()
            self.action_animation = None
            self.load_pet_image()
            self.update()
            return
        
        # 重新绘制宠物图像带挥手效果
        self.load_pet_image()
        temp = self.pet_image.copy()
        painter = QPainter(temp)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 绘制挥手手臂
        arm_angle = [0, 10, 20, 30, 40, 50, 60, 50, 40, 30, 20, 10][self.wave_frame - 1]
        rad = arm_angle * 3.14159 / 180
        hand_x = 120 + int(25 * np.cos(rad))
        hand_y = 40 - int(25 * np.sin(rad))
        
        painter.setPen(QPen(QColor(100, 150, 255), 4))
        painter.drawLine(110, 60, hand_x, hand_y)
        
        # 绘制小手
        painter.setBrush(QBrush(QColor(255, 200, 150)))
        painter.drawEllipse(hand_x - 5, hand_y - 5, 12, 12)
        
        painter.end()
        self.pet_image = temp
        self.update()
    
    def start_jump(self):
        """开始跳跃动画"""
        self.action_animation = "jump"
        self.jump_frame = 0
        self.original_pos = self.pos()
        self.jump_timer = QTimer()
        self.jump_timer.timeout.connect(self.jump_update)
        self.jump_timer.start(40)
    
    def jump_update(self):
        """跳跃动画更新"""
        self.jump_frame += 1
        if self.jump_frame > 24:
            self.jump_timer.stop()
            self.jump_timer.deleteLater()
            self.move(self.original_pos)
            self.action_animation = None
            return
        
        # 跳跃轨迹：正弦波
        height = 35 * np.sin(self.jump_frame * np.pi / 12)
        new_y = self.original_pos.y() - int(height)
        self.move(self.original_pos.x(), new_y)
    
    def start_walk(self):
        """开始踱步动画"""
        self.action_animation = "walk"
        self.walk_frame = 0
        self.walk_direction = random.choice([-1, 1])
        self.walk_original_x = self.x()
        self.walk_timer = QTimer()
        self.walk_timer.timeout.connect(self.walk_update)
        self.walk_timer.start(80)
    
    def walk_update(self):
        """踱步动画更新"""
        self.walk_frame += 1
        if self.walk_frame > 14:
            self.walk_timer.stop()
            self.walk_timer.deleteLater()
            self.move(self.walk_original_x, self.y())
            self.action_animation = None
            self.update()
            return
        
        # 左右摆动
        offset = 8 * np.sin(self.walk_frame * np.pi / 7)
        new_x = self.walk_original_x + int(offset * self.walk_direction)
        
        # 检查屏幕边界
        screen = QApplication.desktop().availableGeometry()
        new_x = max(0, min(new_x, screen.width() - self.width()))
        
        self.move(new_x, self.y())
    
    # ====== 投喂系统 ======
    
    def show_feed_menu(self, position):
        """显示投喂菜单"""
        menu = QMenu(self)
        
        for food in self.food_list:
            action = QAction(food, self)
            action.triggered.connect(lambda checked, f=food: self.feed_pet(f))
            menu.addAction(action)
            
        menu.exec_(position)
    
    def feed_pet(self, food):
        """投喂宠物（含动画）"""
        print(f"投喂: {food}")
        self.last_interaction = datetime.now()
        self.current_state = "standing"
        
        # 开始投喂动画
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
        
        # 创建食物图像
        self.food_image = QPixmap(40, 40)
        self.food_image.fill(Qt.transparent)
        
        painter = QPainter(self.food_image)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 根据食物类型绘制不同颜色
        food_colors = {
            "汉堡": QColor(255, 180, 50),
            "炸鸡": QColor(220, 150, 80),
            "螺蛳粉": QColor(200, 150, 80)
        }
        color = food_colors.get(food, QColor(255, 200, 100))
        
        painter.setBrush(QBrush(color))
        painter.setPen(QPen(QColor(180, 120, 30), 2))
        painter.drawRoundedRect(5, 5, 30, 30, 5, 5)
        
        # 绘制食物标签
        food_labels = {"汉堡": "🍔", "炸鸡": "🍗", "螺蛳粉": "🍜"}
        label = food_labels.get(food, "🍽️")
        painter.drawText(10, 30, label)
        
        painter.end()
        
        # 开始动画定时器
        self.feed_timer = QTimer()
        self.feed_timer.timeout.connect(self.feed_update)
        self.feed_timer.start(50)
    
    def feed_update(self):
        """投喂动画更新"""
        self.food_frame += 1
        self.update()
        
        if self.food_frame > 50:
            self.feed_timer.stop()
            self.feed_timer.deleteLater()
            self.food_animation = None
            self.update()
    
    # ====== 绘制事件 ======
    
    def paintEvent(self, event):
        """绘制事件"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 绘制宠物图像
        painter.drawPixmap(0, 0, self.pet_image)
        
        # 绘制投喂动画
        if self.food_animation and self.food_image:
            # 食物从上方落下
            food_y = -40 + min(self.food_frame * 2, 60)
            if food_y < 80 and self.food_frame < 25:
                food_x = 55
                painter.drawPixmap(food_x, int(food_y), self.food_image)
            
            # 食物名称文字
            if self.food_frame > 20 and self.food_frame < 40:
                painter.setFont(QFont("Arial", 9))
                painter.setPen(QColor(255, 100, 100))
                text_y = int(food_y + 45)
                painter.drawText(60, text_y, self.food_animation)
        
        # 根据状态添加效果
        if self.current_state == "sleeping":
            painter.setFont(QFont("Arial", 14))
            painter.setPen(Qt.blue)
            painter.drawText(55, 25, "😴")
        elif self.current_state == "crouching":
            painter.setFont(QFont("Arial", 10))
            painter.setPen(QColor(100, 100, 100))
            painter.drawText(60, 20, "zzz")
    
    # ====== 状态管理 ======
    
    def check_state(self):
        """检查并更新宠物状态"""
        now = datetime.now()
        idle_time = (now - self.last_interaction).total_seconds()
        
        if idle_time > 120:  # 2分钟无交互
            if self.current_state != "sleeping":
                print("宠物进入睡眠状态")
                self.current_state = "sleeping"
                self.update()
        elif idle_time > 30:  # 30秒无交互
            if self.current_state != "crouching":
                print("宠物进入蹲下状态")
                self.current_state = "crouching"
                self.update()
        else:
            if self.current_state not in ("standing", None):
                self.current_state = "standing"
                self.update()
    
    def closeEvent(self, event):
        """关闭事件"""
        self.save_config()
        event.accept()
    
    # ====== 配置管理 ======
    
    def load_config(self):
        """加载配置"""
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
                    loaded = json.load(f)
                    for key in default_config:
                        if key not in loaded:
                            loaded[key] = default_config[key]
                    return loaded
            except:
                pass
        return default_config.copy()
    
    def save_config(self):
        """保存配置"""
        config = {
            "pet_size": [self.width(), self.height()],
            "position": [self.x(), self.y()],
            "last_state": self.current_state,
            "food_history": self.config.get("food_history", []),
            "user_photo_selected": self.config.get("user_photo_selected", False),
            "use_default_avatar": self.config.get("use_default_avatar", False),
            "user_photo": self.config.get("user_photo"),
            "cartoon_path": self.config.get("cartoon_path")
        }
        
        os.makedirs("config", exist_ok=True)
        with open("config/pet_config.json", 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)


def main():
    """主函数"""
    try:
        print("=" * 40)
        print("  Desktop Pet")
        print("=" * 40)
        print()
        
        app = QApplication(sys.argv)
        app.setQuitOnLastWindowClosed(False)
        
        # 创建宠物窗口
        pet = DesktopPet()
        pet.show()
        
        print("Controls:")
        print("- Left-click: Trigger action")
        print("- Right-click: Feed food")
        print("- Drag: Move pet")
        print("- Tray menu: More options")
        print()
        print("Press Ctrl+C to exit")
        
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")


if __name__ == "__main__":
    main()
