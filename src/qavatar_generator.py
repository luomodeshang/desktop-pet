
"""
Q版小人生成器 + Live2D风格动画引擎
功能：
  1. 从照片提取面部特征 → 生成Q版角色
  2. 提取衣服颜色 → 角色穿同色衣服
  3. Live2D风格动画：呼吸、眨眼、头发飘动、身体微晃
  4. 支持动画帧序列生成（直接给AnimationEngine使用）
"""

import os
import cv2
import numpy as np
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import (
    QPainter, QPixmap, QColor, QPen, QBrush, QFont,
    QPainterPath, QImage
)
from enum import Enum, auto
import math


# ====== 动画参数 ======
# Live2D风格的动画参数，可在运行时修改
class Live2DParams:
    """Live2D风格动画的实时参数"""
    def __init__(self):
        # 呼吸
        self.breath_phase = 0.0       # 呼吸相位 (0~2pi)
        self.breath_amplitude = 0.02  # 呼吸幅度 (身体缩放)
        
        # 眨眼
        self.blink_state = "open"     # open / closing / closed / opening
        self.blink_timer = 0
        self.blink_interval = 180     # 帧间隔（60FPS下约3秒）
        self.blink_duration = 6       # 眨眼持续帧数
        
        # 头发飘动
        self.hair_wave_phase = 0.0
        
        # 身体晃动
        self.body_sway_phase = 0.0
        
        # 面部表情控制 (0.0 ~ 1.0)
        self.eye_open = 1.0           # 1=全开, 0=全闭
        self.mouth_open = 0.0         # 0=闭嘴, 1=张嘴
        self.mouth_width = 1.0        # 嘴巴宽度比例
        self.brow_raise = 0.0         # 眉毛抬起
        self.happiness = 0.5          # 开心程度
        self.anger = 0.0
        self.surprise = 0.0
        self.eye_direction_x = 0.0    # 眼睛看向 -1~1
        self.eye_direction_y = 0.0


# ====== 人脸特征提取（增强版） ======

class FaceFeatures:
    """提取的人脸特征数据（增强版，新增衣物颜色）"""
    def __init__(self):
        self.has_face = False
        self.face_rect = None
        self.skin_color = (0, 0, 0)
        self.hair_color = (0, 0, 0)
        self.eye_color = (0, 0, 0)
        self.lip_color = (0, 0, 0)
        self.clothes_color = (0, 0, 0)    # 新增：衣服主色
        self.clothes_secondary = (0, 0, 0) # 新增：衣服副色
        self.face_shape = "round"
        self.face_width_ratio = 0.85
        self.center_x = 0
        self.center_y = 0
        self.mouth_y = 0
        self.forehead_height = 0.3
        self.eye_spacing = 0.5
        self.eye_size = 0.12
        self.face_ratio = 1.0


def extract_face_features(image_path):
    """从照片中提取人脸特征（增强版：加衣服颜色）"""
    features = FaceFeatures()
    img = cv2.imread(image_path)
    if img is None:
        print(f"无法读取图片: {image_path}")
        return features

    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 人脸检测
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml"
    )
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(80, 80)
    )

    if len(faces) == 0:
        print("未检测到人脸，使用默认特征")
        return features

    x, y, fw, fh = max(faces, key=lambda r: r[2] * r[3])
    features.face_rect = (x, y, fw, fh)
    features.has_face = True
    features.center_x = x + fw // 2
    features.center_y = y + fh // 2

    # --- 皮肤 ---
    cheek_y = y + int(fh * 0.5)
    cheek_region = img[cheek_y:cheek_y + int(fh * 0.2),
                       x + int(fw * 0.2):x + int(fw * 0.8)]
    if cheek_region.size > 0:
        features.skin_color = np.median(cheek_region, axis=(0, 1)).astype(int)
        features.skin_color = np.clip(features.skin_color * 1.15, 0, 255).astype(int)

    # --- 头发 ---
    if y > 10:
        hair_y = max(0, y - int(fh * 0.25))
        hair_region = img[hair_y:max(0, y - 5),
                          x + int(fw * 0.15):x + int(fw * 0.85)]
        if hair_region.size > 0:
            features.hair_color = np.median(hair_region, axis=(0, 1)).astype(int)

    # --- 瞳孔 ---
    eye_y = y + int(fh * 0.28)
    eye_region = img[eye_y:eye_y + int(fh * 0.15),
                     x + int(fw * 0.2):x + int(fw * 0.8)]
    if eye_region.size > 0:
        eye_gray = cv2.cvtColor(eye_region, cv2.COLOR_BGR2GRAY)
        _, dark_mask = cv2.threshold(eye_gray, 60, 255, cv2.THRESH_BINARY_INV)
        if np.sum(dark_mask > 0) > 10:
            dark_pixels = eye_region[dark_mask > 0]
            features.eye_color = np.median(dark_pixels, axis=0).astype(int)
        else:
            features.eye_color = np.array([30, 30, 30])

    # --- 嘴唇 ---
    mouth_y = y + int(fh * 0.55)
    mouth_region = img[mouth_y:mouth_y + int(fh * 0.15),
                       x + int(fw * 0.25):x + int(fw * 0.75)]
    if mouth_region.size > 0:
        b, g, r = cv2.split(mouth_region)
        red_mask = (r > g + 10) & (r > b + 10)
        if np.sum(red_mask) > 10:
            red_pixels = mouth_region[red_mask]
            features.lip_color = np.median(red_pixels, axis=0).astype(int)
        else:
            features.lip_color = np.array([80, 80, 160])

    # ===== 新增：衣服颜色提取 =====
    # 策略：在人脸下方的身体区域（下巴以下）取dominant颜色
    body_y = y + fh + int(fh * 0.05)
    body_h = int(fh * 0.6)
    body_left = max(0, x - int(fw * 0.2))
    body_right = min(w, x + fw + int(fw * 0.2))

    if body_y + body_h < h and body_right > body_left:
        body_region = img[body_y:body_y + body_h,
                         body_left:body_right]
        if body_region.size > 0:
            # 用K-means聚类提取主色和副色
            pixels = body_region.reshape(-1, 3).astype(np.float32)
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
            _, labels, centers = cv2.kmeans(
                pixels, 3, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS
            )
            # 统计每个聚类的像素数
            counts = np.bincount(labels.flatten())
            # 忽略太暗或太亮的聚类（可能是背景）
            valid = []
            for i, c in enumerate(counts):
                color = centers[i].astype(int)
                brightness = np.mean(color)
                if 30 < brightness < 240:  # 排除纯黑/纯白
                    valid.append((c, color))
            if valid:
                valid.sort(key=lambda x: -x[0])
                features.clothes_color = tuple(valid[0][1])
                if len(valid) > 1:
                    features.clothes_secondary = tuple(valid[1][1])
                else:
                    features.clothes_secondary = features.clothes_color

    # 如果衣服颜色没提取到，用默认色
    if np.sum(features.clothes_color) == 0:
        # 基于肤色的搭配色
        skin = features.skin_color
        if np.mean(skin) > 150:
            features.clothes_color = (80, 100, 180)   # 蓝色系
            features.clothes_secondary = (180, 180, 200)
        else:
            features.clothes_color = (60, 80, 160)
            features.clothes_secondary = (140, 140, 180)

    # --- 脸型 ---
    face_ratio = fw / fh
    features.face_ratio = face_ratio
    if face_ratio > 0.95:
        features.face_shape = "round"
    elif face_ratio > 0.85:
        features.face_shape = "oval"
    elif face_ratio > 0.75:
        features.face_shape = "square"
    else:
        features.face_shape = "heart"

    features.mouth_y = int(fh * 0.62)
    return features


# ====== Live2D风格角色渲染器 ======

class QAvatarRenderer:
    """
    Q版小人 + Live2D风格动画渲染器
    支持动画参数驱动，每帧可以传入不同的 Live2DParams
    """

    HEAD_RATIO = 0.65

    def __init__(self, features: FaceFeatures):
        self.features = features

    def render(self, canvas_size=(150, 200), params: Live2DParams = None) -> QPixmap:
        """
        渲染当前帧
        params: 动画参数（为None则用默认值）
        """
        if params is None:
            params = Live2DParams()

        cw, ch = canvas_size
        pix = QPixmap(cw, ch)
        pix.fill(Qt.transparent)
        painter = QPainter(pix)
        painter.setRenderHint(QPainter.Antialiasing)

        # 呼吸 → 整体微缩放
        breath_scale = 1.0 + params.breath_amplitude * math.sin(params.breath_phase)
        body_sway = 2.0 * math.sin(params.body_sway_phase)

        total_height = int(ch * 0.90)
        head_height = int(total_height * self.HEAD_RATIO)
        body_height = total_height - head_height
        head_size = min(cw - 20, head_height)
        head_x = (cw - head_size) // 2
        head_y = 5

        body_top = head_y + head_size - 10
        body_width = int(head_size * 0.55)
        body_width = int(body_width * breath_scale)  # 呼吸影响宽度
        body_height = min(body_height, ch - body_top - 5)

        # ---- 身体 ----
        self._draw_body(painter, QPoint(cw // 2 + int(body_sway), body_top),
                       body_width, body_height, params)

        # ---- 头部 ----
        head_offset = int(2 * math.sin(params.breath_phase))  # 呼吸时头微微上下
        self._draw_head(painter, QPoint(head_x, head_y + head_offset),
                       head_size, params)

        # ---- 头发（带飘动） ----
        self._draw_hair(painter, QPoint(head_x, head_y + head_offset),
                       head_size, params)

        painter.end()
        return pix

    def _draw_head(self, painter, top_left, size, params):
        """绘制头部（带Live2D风格表情）"""
        x, y = top_left.x(), top_left.y()
        skin = self.features.skin_color
        face_w = size
        face_h = int(size * 1.05)

        path = QPainterPath()
        path.addEllipse(x, y, face_w, face_h)

        painter.setBrush(QBrush(QColor(int(skin[2]), int(skin[1]), int(skin[0]), 255)))
        painter.setPen(QPen(QColor(int(skin[2] * 0.7), int(skin[1] * 0.7), int(skin[0] * 0.7)), 2))
        painter.drawPath(path)

        # 眉毛（受情绪影响）
        self._draw_eyebrows(painter, x, y, face_w, face_h, params)

        # 眼睛（受眨眼和情绪影响）
        self._draw_eyes(painter, x, y, face_w, face_h, params)

        # 嘴巴（受张嘴和情绪影响）
        self._draw_mouth(painter, x, y, face_w, face_h, params)

        # 腮红（开心时更红）
        self._draw_blush(painter, x, y, face_w, face_h, params)

    def _draw_eyes(self, painter, fx, fy, fw, fh, params):
        """绘制Q版大眼睛（Live2D：眨眼+视线移动+情绪）"""
        eye_color = self.features.eye_color
        eye_y = fy + int(fh * 0.35)
        eye_size_w = int(fw * 0.15)
        eye_size_h = int(fh * 0.18)
        eye_spacing = int(fw * 0.18)
        
        # 眨眼控制
        blink = params.eye_open  # 1=全开, 0=全闭
        current_eye_h = max(1, int(eye_size_h * blink))
        
        # 视线方向
        look_x = int(params.eye_direction_x * 3)
        look_y = int(params.eye_direction_y * 2)

        cx = fx + fw // 2
        left_eye_cx = cx - eye_spacing - eye_size_w // 2
        right_eye_cx = cx + eye_spacing

        for base_cx in [left_eye_cx, right_eye_cx]:
            if blink > 0.15:
                # 眼白
                painter.setBrush(QBrush(Qt.white))
                painter.setPen(QPen(QColor(60, 60, 60), 2))
                painter.drawEllipse(base_cx - eye_size_w // 2, eye_y - current_eye_h // 2,
                                  eye_size_w, current_eye_h)

                # 瞳孔
                pupil_r = max(2, eye_size_w // 2 - 1)
                pupil_r = int(pupil_r * (0.6 + blink * 0.4))
                eye_cx = base_cx + look_x
                eye_cy = eye_y + look_y
                
                painter.setBrush(QBrush(QColor(
                    min(int(eye_color[2]) + 20, 255),
                    min(int(eye_color[1]) + 20, 255),
                    min(int(eye_color[0]) + 20, 255)
                )))
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(eye_cx - pupil_r + 1, eye_cy - pupil_r + 1,
                                  pupil_r * 2, pupil_r * 2)

                # 高光
                highlight_r = max(1, pupil_r - 2)
                painter.setBrush(QBrush(Qt.white))
                painter.drawEllipse(eye_cx - highlight_r // 2 + look_x,
                                  eye_cy - highlight_r // 2 - 1 + look_y,
                                  highlight_r, highlight_r)
                
                # 第二高光
                painter.setBrush(QBrush(QColor(255, 255, 255, 120)))
                painter.drawEllipse(eye_cx + pupil_r // 4 + look_x,
                                  eye_cy + pupil_r // 4 + look_y, 3, 3)
            else:
                # 闭眼（一条弧线）
                painter.setPen(QPen(QColor(60, 40, 30), 2))
                painter.drawArc(base_cx - eye_size_w // 2, eye_y - 2,
                              eye_size_w, 8, 0, 180 * 16)

    def _draw_eyebrows(self, painter, fx, fy, fw, fh, params):
        """绘制眉毛（受情绪驱动）"""
        brow_y = fy + int(fh * 0.28)
        brow_w = int(fw * 0.12)
        brow_spacing = int(fw * 0.18)
        cx = fx + fw // 2

        # 惊讶时眉毛抬高，生气时压低
        raise_amount = params.brow_raise * 5 - params.anger * 3 + params.surprise * 6

        painter.setPen(QPen(QColor(60, 40, 30), 2))
        painter.setBrush(Qt.NoBrush)

        for side, sign in [("left", -1), ("right", 1)]:
            bx = cx + sign * brow_spacing
            if side == "left":
                bx -= brow_w
            y_offset = int(raise_amount)
            if params.anger > 0.5:
                # 生气：眉尾下压
                end_offset = 3 if side == "left" else -3
            else:
                end_offset = 0

            path = QPainterPath()
            path.moveTo(bx, brow_y + y_offset)
            path.cubicTo(bx + brow_w // 3, brow_y + y_offset - 2,
                        bx + brow_w * 2 // 3, brow_y + y_offset + 1 + end_offset,
                        bx + brow_w + 2, brow_y + y_offset + 2 + end_offset)
            painter.drawPath(path)

    def _draw_mouth(self, painter, fx, fy, fw, fh, params):
        """绘制嘴巴（Live2D：张嘴+微笑）"""
        lip = self.features.lip_color
        mouth_y = fy + int(fh * 0.62)
        cx = fx + fw // 2
        
        mouth_open = params.mouth_open
        happiness = params.happiness
        surprise = params.surprise

        lip_r = int(lip[2])
        lip_g = int(lip[1])
        lip_b = int(lip[0])

        if mouth_open > 0.1 or surprise > 0.5:
            # 张嘴（惊讶/说话/打哈欠）
            open_amount = max(mouth_open, surprise * 0.8)
            mouth_w = int(fw * 0.22)
            mouth_h = int(fw * 0.18 * open_amount)
            
            painter.setBrush(QBrush(QColor(
                min(lip_r + 30, 255), min(lip_g + 20, 255), min(lip_b + 20, 255)
            )))
            painter.setPen(QPen(QColor(lip_r, lip_g, lip_b), 1))
            painter.drawEllipse(cx - mouth_w // 2, mouth_y - mouth_h // 2,
                              mouth_w, mouth_h)
            
            # 口腔内部（深色）
            if mouth_h > 4:
                inner_h = mouth_h - 4
                painter.setBrush(QBrush(QColor(60, 20, 20)))
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(cx - mouth_w // 2 + 2,
                                  mouth_y - inner_h // 2 + 1,
                                  mouth_w - 4, inner_h - 2)
        else:
            # 微笑（弧度受开心程度影响）
            smile_arc = int(60 + happiness * 60)  # 60°~120°
            painter.setPen(QPen(QColor(lip_r, lip_g, lip_b), 2))
            painter.setBrush(Qt.NoBrush)
            painter.drawArc(cx - int(fw * 0.1), mouth_y - 3,
                          int(fw * 0.2), int(fw * 0.1),
                          0, smile_arc * 16)

    def _draw_blush(self, painter, fx, fy, fw, fh, params):
        """绘制腮红（开心时加深）"""
        blush_y = fy + int(fh * 0.52)
        blush_r = int(fw * 0.06)
        cx = fx + fw // 2
        spacing = int(fw * 0.25)
        
        # 开心/害羞时腮红更明显
        intensity = min(80, int(60 + params.happiness * 40))
        
        painter.setBrush(QBrush(QColor(255, 150, 150, intensity)))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(cx - spacing - blush_r, blush_y - blush_r // 2,
                          blush_r * 2, blush_r)
        painter.drawEllipse(cx + spacing - blush_r, blush_y - blush_r // 2,
                          blush_r * 2, blush_r)

    def _draw_hair(self, painter, top_left, size, params):
        """绘制头发（带飘动效果）"""
        x, y = top_left.x(), top_left.y()
        hair = self.features.hair_color
        if not self.features.has_face:
            hair = np.array([50, 40, 30])

        hair_color = QColor(int(hair[2]), int(hair[1]), int(hair[0]))
        wave_phase = params.hair_wave_phase

        # 主头发
        hair_path = QPainterPath()
        hair_path.moveTo(x + int(size * 0.02), y + int(size * 0.25))
        
        # 头发飘动——控制点随相位左右摆动
        sway = 4 * math.sin(wave_phase)
        
        hair_path.cubicTo(
            x + int(size * 0.02) + int(sway), y - int(size * 0.05),
            x + size - int(size * 0.02) + int(sway), y - int(size * 0.05),
            x + size - int(size * 0.02), y + int(size * 0.25)
        )

        painter.setBrush(QBrush(hair_color))
        painter.setPen(Qt.NoPen)
        painter.drawPath(hair_path)

        # 刘海（带飘动）
        painter.setPen(QPen(hair_color, 3))
        painter.setBrush(Qt.NoBrush)
        bangs_count = 5
        for i in range(bangs_count):
            bx = x + int(size * (0.15 + i * 0.16))
            by = y + int(size * 0.12)
            # 刘海每根微微摆动
            sway_i = 2 * math.sin(wave_phase + i * 1.2)
            end_y = y + int(size * (0.22 + (i % 2) * 0.06))
            painter.drawLine(bx, by, bx + int(sway_i), end_y)

        # 两侧头发（侧发飘动）
        side_sway = 3 * math.sin(wave_phase + 2.0)
        painter.setPen(QPen(hair_color, 4))
        # 左侧
        painter.drawLine(x, y + int(size * 0.2),
                        x + int(side_sway), y + int(size * 0.55))
        # 右侧
        painter.drawLine(x + size, y + int(size * 0.2),
                        x + size + int(-side_sway), y + int(size * 0.55))

    def _draw_body(self, painter, center, width, height, params):
        """绘制Q版小身体（带衣服颜色和呼吸微动）"""
        cx, cy = center.x(), center.y()
        
        # 从特征获取衣服颜色
        clothes = self.features.clothes_color
        clothes2 = self.features.clothes_secondary

        main_color = QColor(
            min(int(clothes[2]), 255),
            min(int(clothes[1]), 255),
            min(int(clothes[0]), 255)
        )
        accent_color = QColor(
            min(int(clothes2[2]), 255),
            min(int(clothes2[1]), 255),
            min(int(clothes2[0]), 255)
        )

        # 衣服主体
        body_rect = QRect(cx - width // 2, cy, width, height)
        painter.setBrush(QBrush(main_color))
        painter.setPen(QPen(accent_color, 1))
        painter.drawRoundedRect(body_rect, 10, 10)

        # 衣领配色（副色）
        collar_h = int(height * 0.12)
        collar_rect = QRect(cx - width // 2, cy, width, collar_h)
        painter.setBrush(QBrush(accent_color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(collar_rect, 8, 8)

        # 衣领V字装饰
        painter.setPen(QPen(QColor(255, 255, 255, 100), 2))
        painter.drawLine(cx - width // 4, cy + int(height * 0.12),
                        cx, cy + int(height * 0.25))
        painter.drawLine(cx + width // 4, cy + int(height * 0.12),
                        cx, cy + int(height * 0.25))

        # 手臂（两边 + 带呼吸微动）
        arm_color = QColor(
            min(int(clothes[2] * 0.8), 255),
            min(int(clothes[1] * 0.8), 255),
            min(int(clothes[0] * 0.8), 255)
        )
        arm_sway = int(2 * math.sin(params.body_sway_phase))
        
        painter.setBrush(QBrush(arm_color))
        painter.setPen(Qt.NoPen)
        
        # 左手
        painter.drawRoundedRect(
            cx - width // 2 - 8 + arm_sway, cy + int(height * 0.15),
            10, int(height * 0.25), 4, 4
        )
        # 右手
        painter.drawRoundedRect(
            cx + width // 2 - 2 - arm_sway, cy + int(height * 0.15),
            10, int(height * 0.25), 4, 4
        )

        # 小脚
        foot_color = accent_color
        painter.setBrush(QBrush(foot_color))
        painter.drawRoundedRect(
            cx - width // 4 - 5, cy + height - 4,
            width // 4, 6, 3, 3
        )
        painter.drawRoundedRect(
            cx + width // 4 - 5, cy + height - 4,
            width // 4, 6, 3, 3
        )


# ====== Live2D风格动画帧生成器 ======

class Live2DAnimator:
    """
    Live2D风格动画控制器
    自动管理呼吸、眨眼、头发飘动参数
    每一帧调用 update() 更新参数，返回当前帧的 QPixmap
    """
    
    def __init__(self, renderer: QAvatarRenderer, canvas_size=(150, 200)):
        self.renderer = renderer
        self.canvas_size = canvas_size
        self.params = Live2DParams()
        self.frame_count = 0
        
        # 随机眨眼间隔（3~5秒）
        self.blink_counter = 0
        self.next_blink = random.randint(150, 300)
        
        # 当前情绪
        self.mood = "neutral"  # neutral / happy / surprised / eating
        
    def update(self) -> QPixmap:
        """更新动画参数，返回当前帧"""
        self.frame_count += 1
        f = self.frame_count
        
        # --- 呼吸（持续循环） ---
        self.params.breath_phase = f * 0.05
        self.params.body_sway_phase = f * 0.02
        
        # --- 头发飘动（持续循环） ---
        self.params.hair_wave_phase = f * 0.06
        
        # --- 眨眼（间歇） ---
        self.blink_counter += 1
        if self.blink_counter >= self.next_blink:
            self.blink_counter = 0
            self.next_blink = random.randint(150, 300)
        
        if self.blink_counter < 3:
            self.params.eye_open = max(0.1, 1.0 - self.blink_counter * 0.3)
        elif self.blink_counter < 6:
            self.params.eye_open = min(1.0, 0.1 + (self.blink_counter - 3) * 0.3)
        else:
            self.params.eye_open = 1.0
        
        # --- 嘴部（根据情绪） ---
        if self.mood == "surprised":
            self.params.mouth_open = 0.6 + 0.2 * math.sin(f * 0.1)
            self.params.brow_raise = 0.8
            self.params.happiness = 0.3
        elif self.mood == "happy":
            self.params.mouth_open = 0.3 + 0.15 * math.sin(f * 0.08)
            self.params.brow_raise = 0.3
            self.params.happiness = 0.9
            self.params.surprise = 0.0
        elif self.mood == "eating":
            self.params.mouth_open = 0.5 + 0.4 * math.sin(f * 0.2)
            self.params.brow_raise = 0.0
            self.params.happiness = 0.7
        else:
            # neutral: 自然呼吸微动
            self.params.mouth_open = 0.05 + 0.03 * math.sin(f * 0.04)
            self.params.brow_raise = 0.0
            self.params.happiness = 0.5
            self.params.surprise = 0.0
        
        # --- 视线（偶尔扫视） ---
        self.params.eye_direction_x = 0.3 * math.sin(f * 0.015)
        self.params.eye_direction_y = 0.1 * math.sin(f * 0.02)
        
        return self.renderer.render(self.canvas_size, self.params)
    
    def set_mood(self, mood):
        """设置情绪状态"""
        if mood in ("neutral", "happy", "surprised", "eating"):
            self.mood = mood
    
    def get_params_snapshot(self) -> dict:
        """获取当前参数快照（用于保存/恢复）"""
        return {
            "eye_open": self.params.eye_open,
            "mouth_open": self.params.mouth_open,
            "happiness": self.params.happiness,
            "mood": self.mood,
        }


# ====== 便捷接口 ======

def create_qavatar(input_path, output_path, canvas_size=(150, 200)):
    """从照片创建Q版角色静态图"""
    features = extract_face_features(input_path)
    renderer = QAvatarRenderer(features)
    pixmap = renderer.render(canvas_size)
    pixmap.save(output_path)
    print(f"Q版角色已保存: {output_path}")
    return pixmap


def create_qavatar_pixmap(image_path, canvas_size=(150, 200)):
    """从照片创建Q版角色，返回QPixmap"""
    features = extract_face_features(image_path)
    renderer = QAvatarRenderer(features)
    return renderer.render(canvas_size)


# 测试入口
if __name__ == "__main__":
    import sys
    import random
    from PyQt5.QtWidgets import QApplication
    
    if len(sys.argv) > 1:
        app = QApplication(sys.argv)
        input_path = sys.argv[1]
        output_path = sys.argv[2] if len(sys.argv) > 2 else "qavatar_output.png"
        
        print(f"输入: {input_path}")
        print(f"输出: {output_path}")
        
        # 特征提取
        features = extract_face_features(input_path)
        print(f"检测到人脸: {features.has_face}")
        print(f"脸型: {features.face_shape}")
        print(f"肤色: {features.skin_color}")
        print(f"发色: {features.hair_color}")
        print(f"衣服色: {features.clothes_color}")
        print(f"衣服副色: {features.clothes_secondary}")
        
        # 渲染静态图
        pix = create_qavatar(input_path, output_path)
        print(f"完成! 尺寸: {pix.width()}x{pix.height()}")
