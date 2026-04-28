
"""
动画引擎 - 统一FPS帧循环 + 帧缓存系统
替代原来独立的 wave/jump/walk/feed QTimer，所有动画在单个主循环中调度
"""

import numpy as np
from enum import Enum, auto
from PyQt5.QtCore import QTimer, QPoint, Qt
from PyQt5.QtGui import QPixmap, QPainter, QColor, QPen, QBrush, QFont


class AnimationType(Enum):
    NONE = auto()
    WAVE = auto()
    JUMP = auto()
    WALK = auto()
    FEED = auto()


class AnimState:
    def __init__(self):
        self.anim_type = AnimationType.NONE
        self.frame = 0
        self.total_frames = 0
        self.is_playing = False
        self.loop = False
        self.original_pos = None
        self.direction = 1
        self.original_x = 0
        self.food_name = ""

    def start(self, anim_type, total_frames, loop=False):
        self.anim_type = anim_type
        self.frame = 0
        self.total_frames = total_frames
        self.is_playing = True
        self.loop = loop

    def stop(self):
        self.is_playing = False
        self.frame = 0
        self.anim_type = AnimationType.NONE

    def advance(self):
        if not self.is_playing:
            return False
        self.frame += 1
        if self.frame >= self.total_frames:
            if self.loop:
                self.frame = 0
                return True
            else:
                self.stop()
                return False
        return True


class FrameGenerator:
    def __init__(self, pet_size=(150, 150)):
        self.pet_size = pet_size
        self.base_pixmap = None
        self._cache = {}

    def set_base_image(self, pixmap):
        self.base_pixmap = pixmap

    def set_pet_size(self, w, h):
        self.pet_size = (w, h)
        self._cache.clear()

    def need_rebuild(self, anim_type):
        return anim_type not in self._cache or len(self._cache[anim_type]) == 0

    def get_frame(self, anim_type, frame):
        frames = self._cache.get(anim_type, [])
        if not frames:
            return None
        return frames[frame % len(frames)]

    def prerender_wave(self):
        frames = []
        w, h = self.pet_size
        arm_angles = [0, 10, 20, 30, 40, 50, 60, 50, 40, 30, 20, 10, 0]
        for angle in arm_angles:
            pix = self._copy_base()
            if pix:
                painter = QPainter(pix)
                painter.setRenderHint(QPainter.Antialiasing)
                rad = angle * 3.14159 / 180
                hand_x = w - 30 + int(25 * np.cos(rad))
                hand_y = 40 - int(25 * np.sin(rad))
                painter.setPen(QPen(QColor(100, 150, 255), 4))
                painter.drawLine(w - 40, 60, hand_x, hand_y)
                painter.setBrush(QBrush(QColor(255, 200, 150)))
                painter.drawEllipse(hand_x - 5, hand_y - 5, 12, 12)
                painter.end()
            frames.append(pix)
        self._cache[AnimationType.WAVE] = frames

    def prerender_feed(self):
        frames = []
        w, h = self.pet_size
        food_name = getattr(self, '_feed_food_type', '').lower()
        for i in range(51):
            pix = self._copy_base()
            if pix:
                painter = QPainter(pix)
                painter.setRenderHint(QPainter.Antialiasing)
                progress = i / 50
                food_y = -40 + min(i * 2, 60)
                if food_y < 80 and progress < 0.5:
                    food_x = w // 2 - 20
                    if 'burger' in food_name and 'fried' not in food_name and 'chicken' not in food_name:
                        # Burger style
                        painter.setBrush(QBrush(QColor(220, 160, 80)))
                        painter.setPen(Qt.NoPen)
                        painter.drawEllipse(food_x, int(food_y), 40, 12)
                        painter.setBrush(QBrush(QColor(140, 80, 30)))
                        painter.drawRect(food_x + 3, int(food_y + 10), 34, 10)
                        painter.setBrush(QBrush(QColor(220, 160, 80)))
                        painter.drawEllipse(food_x, int(food_y + 18), 40, 12)
                        # Lettuce line
                        painter.setPen(QPen(QColor(100, 200, 80), 2))
                        painter.drawLine(food_x + 10, int(food_y + 15), food_x + 30, int(food_y + 15))
                    elif 'fried' in food_name or 'chicken' in food_name:
                        # Drumstick
                        painter.setBrush(QBrush(QColor(200, 130, 50)))
                        painter.setPen(Qt.NoPen)
                        painter.drawEllipse(food_x + 4, int(food_y + 2), 32, 18)
                        painter.setBrush(QBrush(QColor(220, 160, 100)))
                        painter.drawRoundedRect(food_x + 8, int(food_y), 16, 22, 4, 4)
                        # Bone line
                        painter.setPen(QPen(QColor(180, 140, 100), 2))
                        painter.drawLine(food_x + 30, int(food_y + 10), food_x + 38, int(food_y + 14))
                    else:
                        # Noodles bowl
                        painter.setBrush(QBrush(QColor(180, 140, 100)))
                        painter.setPen(Qt.NoPen)
                        painter.drawRoundedRect(food_x, int(food_y), 40, 28, 8, 8)
                        painter.setBrush(QBrush(QColor(230, 190, 80)))
                        painter.drawEllipse(food_x + 4, int(food_y + 4), 32, 16)
                        # Noodle lines
                        painter.setPen(QPen(QColor(160, 120, 70), 2))
                        painter.drawLine(food_x + 8, int(food_y + 10), food_x + 32, int(food_y + 10))
                        painter.drawLine(food_x + 12, int(food_y + 14), food_x + 28, int(food_y + 14))
                        painter.setPen(QPen(QColor(200, 50, 50), 2))
                        painter.drawLine(food_x + 10, int(food_y + 18), food_x + 30, int(food_y + 18))
                painter.end()
            frames.append(pix)
        self._cache[AnimationType.FEED] = frames
    def prerender_jump(self):
        frames = []
        w, h = self.pet_size
        total = 30
        for i in range(total):
            pix = QPixmap(w, h)
            pix.fill(Qt.transparent)
            painter = QPainter(pix)
            painter.setRenderHint(QPainter.Antialiasing)
            progress = i / total
            jump_y = int(100 * np.sin(progress * np.pi))
            if progress < 0.15:
                squash = 1.0 - 0.08 * (progress / 0.15)
            elif progress < 0.5:
                squash = 0.92 - 0.08 * ((progress - 0.15) / 0.35)
            elif progress < 0.85:
                squash = 0.84 + 0.08 * ((progress - 0.5) / 0.35)
            else:
                squash = 0.92 + 0.08 * ((progress - 0.85) / 0.15)
            scale_y = squash
            scale_x = 1.0 / squash if squash > 0 else 1.0
            shadow_size = 0.5 + 0.5 * (1.0 - progress) if progress < 0.5 else 0.5 + 0.5 * progress
            shadow_alpha = int(max(20, 100 - int(jump_y * 1.2)))
            painter.setBrush(QBrush(QColor(0, 0, 0, shadow_alpha)))
            painter.setPen(Qt.NoPen)
            sw = int(w * 0.45 * shadow_size)
            painter.drawEllipse(w//2 - sw//2, h - 8, sw, 6)
            if self.base_pixmap:
                sw2 = max(1, int(w * scale_x))
                sh2 = max(1, int(h * scale_y))
                scaled = self.base_pixmap.scaled(sw2, sh2, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                draw_x = (w - scaled.width()) // 2
                draw_y = h - scaled.height() - jump_y - 10
                painter.drawPixmap(draw_x, draw_y, scaled)
            painter.end()
            frames.append(pix)
        self._cache[AnimationType.JUMP] = frames

    def prerender_walk(self):
        frames = []
        w, h = self.pet_size
        total = 20
        for i in range(total):
            pix = QPixmap(w, h)
            pix.fill(Qt.transparent)
            painter = QPainter(pix)
            painter.setRenderHint(QPainter.Antialiasing)
            angle = i * 2 * np.pi / total
            offset_x = int(22 * np.sin(angle))
            bounce_y = int(5 * abs(np.sin(angle)))
            if self.base_pixmap:
                scaled = self.base_pixmap.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                draw_x = (w - scaled.width()) // 2 + offset_x
                draw_y = h - scaled.height() - bounce_y
                painter.drawPixmap(draw_x, draw_y, scaled)
                foot_offset = int(12 * np.sin(angle))
                foot_color = QColor(70, 50, 35)
                painter.setBrush(QBrush(foot_color))
                painter.setPen(Qt.NoPen)
                painter.drawRoundedRect(w//2 + foot_offset - 8, h - 10, 8, 8, 3, 3)
                painter.drawRoundedRect(w//2 - foot_offset, h - 10, 8, 8, 3, 3)
                painter.setPen(QPen(QColor(200, 200, 200, 100), 1))
                painter.drawLine(draw_x - 2, h - 5, draw_x + scaled.width() + 2, h - 5)
            painter.end()
            frames.append(pix)
        self._cache[AnimationType.WALK] = frames

    def prerender_none(self):
        pix = self._copy_base()
        self._cache[AnimationType.NONE] = [pix]

    def _copy_base(self):
        if self.base_pixmap:
            return QPixmap(self.base_pixmap)
        pix = QPixmap(*self.pet_size)
        pix.fill(Qt.transparent)
        return pix


class AnimationEngine:
    FPS = 30
    FRAME_MS = 1000 // FPS

    ANIM_CONFIG = {
        AnimationType.WAVE: {"frames": 13, "loop": False},
        AnimationType.JUMP: {"frames": 30, "loop": False},
        AnimationType.WALK: {"frames": 20, "loop": False},
        AnimationType.FEED: {"frames": 51, "loop": False},
    }

    def __init__(self, frame_generator=None, on_render=None):
        self.generator = frame_generator
        self.state = AnimState()
        self.on_render = on_render
        self.is_running = True
        self._timer = QTimer()
        self._timer.timeout.connect(self._tick)
        self._timer.setTimerType(Qt.PreciseTimer)
        self._timer.start(self.FRAME_MS)
        if self.generator:
            self._ensure_cache(AnimationType.NONE)

    def _tick(self):
        if not self.is_running:
            return
        if self.state.is_playing:
            if self.state.anim_type != AnimationType.NONE:
                still_playing = self.state.advance()
                if not still_playing:
                    self.state.anim_type = AnimationType.NONE
                    self.state.is_playing = True
                if self.on_render:
                    self.on_render(self.state.anim_type, self.state.frame)
                return
            # Idle loop: advance frame counter for visual variety
            self.state.frame = (self.state.frame + 1) % 1000000
            if self.on_render:
                self.on_render(AnimationType.NONE, 0)

    def play(self, anim_type, extra_params=None):
        if anim_type == AnimationType.NONE:
            return
        config = self.ANIM_CONFIG.get(anim_type, {"frames": 10, "loop": False})
        self.state.start(anim_type, config["frames"], config["loop"])
        if extra_params:
            for k, v in extra_params.items():
                setattr(self.state, k, v)
        self._ensure_cache(anim_type)

    def _ensure_cache(self, anim_type):
        if self.generator is None:
            return
        if self.generator.need_rebuild(anim_type):
            if anim_type == AnimationType.WAVE:
                self.generator.prerender_wave()
            elif anim_type == AnimationType.FEED:
                self.generator.prerender_feed()
            elif anim_type == AnimationType.JUMP:
                self.generator.prerender_jump()
            elif anim_type == AnimationType.WALK:
                self.generator.prerender_walk()
            elif anim_type == AnimationType.NONE:
                self.generator.prerender_none()

    def get_current_frame(self):
        if self.generator is None:
            return None
        if self.state.is_playing and self.state.anim_type != AnimationType.NONE:
            return self.generator.get_frame(self.state.anim_type, self.state.frame)
        return self.generator.get_frame(AnimationType.NONE, 0)

    def reset_idle_timer(self):
        pass

    def clear_cache(self):
        self.generator._cache.clear()
        self._ensure_cache(AnimationType.WAVE)
        self._ensure_cache(AnimationType.FEED)
        self._ensure_cache(AnimationType.NONE)

    def stop(self):
        self.is_running = False
        self._timer.stop()
        self.state.stop()
