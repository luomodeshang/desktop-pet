
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
        for i in range(51):
            pix = self._copy_base()
            if pix:
                painter = QPainter(pix)
                painter.setRenderHint(QPainter.Antialiasing)
                food_y = -40 + min(i * 2, 60)
                if food_y < 80 and i < 25:
                    food_x = w // 2 - 20
                    painter.setBrush(QBrush(QColor(255, 180, 50)))
                    painter.setPen(QPen(QColor(180, 120, 30), 2))
                    painter.drawRoundedRect(food_x, int(food_y), 30, 30, 5, 5)
                if 20 < i < 40:
                    painter.setFont(QFont("Arial", 14))
                    painter.setPen(QColor(255, 100, 100))
                    painter.drawText(w // 2 - 10, int(food_y + 45), "\U0001f60b")
                painter.end()
            frames.append(pix)
        self._cache[AnimationType.FEED] = frames

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
        AnimationType.JUMP: {"frames": 25, "loop": False},
        AnimationType.WALK: {"frames": 15, "loop": False},
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
        if self.state.is_playing and self.state.anim_type != AnimationType.NONE:
            still_playing = self.state.advance()
            if not still_playing:
                self.state.anim_type = AnimationType.NONE
                self.state.is_playing = True
            if self.on_render:
                self.on_render(self.state.anim_type, self.state.frame)
        else:
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
