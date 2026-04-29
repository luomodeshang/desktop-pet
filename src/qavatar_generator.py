#!/usr/bin/env python3
"""
Q版小人生成器 V4 + Live2D风格动画引擎 (MediaPipe FaceMesh版)
基于MediaPipe 478点3D面部网格，提取精确面部特征并Q版化渲染

功能：
  1. MediaPipe FaceMesh: 478点面部关键点检测（4MB onnx模型）
  2. 精确脸型：基于实际下颌线/下巴轮廓的Q版化
  3. 个性化五官：眼型、嘴型、鼻型基于实际landmarks映射
  4. Live2D风格动画：呼吸、眨眼、头发飘动、表情驱动
"""

import os, random, math
import numpy as np
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import (
    QPainter, QPixmap, QColor, QPen, QBrush, QFont,
    QPainterPath, QImage
)
from enum import Enum, auto

try:
    import cv2
except ImportError:
    cv2 = None

try:
    from mediapipe.tasks.python.vision import FaceLandmarker, FaceLandmarkerOptions, RunningMode
    from mediapipe.tasks.python import BaseOptions
    from mediapipe import Image, ImageFormat
    _HAS_MEDIAPIPE = True
except ImportError:
    # 自动安装 MediaPipe（无编程基础用户友好）
    print("[INFO] MediaPipe not found. Auto-installing... (one-time)")
    try:
        import subprocess, sys, os
        
        # Try local whl first (for users without internet access)
        _script_dir = os.path.dirname(os.path.abspath(__file__))
        local_whl = os.path.join(os.path.dirname(_script_dir), "deps", "mediapipe-0.10.21-cp39-cp39-win_amd64.whl")
        if os.path.exists(local_whl):
            print("[INFO] Found local package, installing...")
            # Use mirror for dependency resolution (Chinese network friendly)
            mirrors = ["https://pypi.tuna.tsinghua.edu.cn/simple", "https://mirrors.aliyun.com/pypi/simple"]
            installed = False
            for mirror in mirrors:
                try:
                    subprocess.check_call(
                        [sys.executable, "-m", "pip", "install", local_whl, "-i", mirror, "--quiet"]
                    )
                    installed = True
                    break
                except:
                    continue
            if not installed:
                subprocess.check_call([sys.executable, "-m", "pip", "install", local_whl, "--quiet"])
        else:
            mirrors = ["https://pypi.tuna.tsinghua.edu.cn/simple", "https://mirrors.aliyun.com/pypi/simple"]
            installed = False
            for mirror in mirrors:
                try:
                    subprocess.check_call(
                        [sys.executable, "-m", "pip", "install", "mediapipe", "-i", mirror, "--quiet"]
                    )
                    installed = True
                    break
                except:
                    continue
            if not installed:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", "mediapipe", "--quiet"]
                )
        print("[OK] MediaPipe installed! Restarting import...")
        from mediapipe.tasks.python.vision import FaceLandmarker, FaceLandmarkerOptions, RunningMode
        from mediapipe.tasks.python import BaseOptions
        from mediapipe import Image, ImageFormat
        _HAS_MEDIAPIPE = True
    except Exception as auto_e:
        print(f"[INFO] Auto-install failed: {auto_e}")
        print("[INFO] Using OpenCV fallback (limited features)")
        print("[INFO] If network is restricted, download whl manually and place in deps/ folder")
        _HAS_MEDIAPIPE = False

# ====== Live2D动画参数 ======
class Live2DParams:
    """Live2D风格动画的实时参数"""
    def __init__(self):
        self.breath_phase = 0.0
        self.breath_amplitude = 0.02
        self.body_sway_phase = 0.0
        self.body_sway_amplitude = 1.5
        self.eye_open = 1.0
        self.eye_direction_x = 0.0
        self.eye_direction_y = 0.0
        self.hair_wave_phase = 0.0
        self.happiness = 0.5
        self.surprise = 0.0
        self.anger = 0.0
        self.mouth_open = 0.0
        self.brow_raise = 0.0

class AnimationType(Enum):
    NONE = auto()
    IDLE = auto()
    BLINK = auto()
    SPEAK = auto()


# ====== 面部特征数据结构 ======
class FaceFeatures:
    """从照片提取的面部特征数据，供渲染器使用"""
    def __init__(self):
        self.has_face = False
        self.mediapipe_detected = False  # True = MediaPipe, False = OpenCV fallback
        
        # === 从照片提取的颜色 ===
        self.skin_color = (200, 170, 150)    # BGR
        self.hair_color = (50, 40, 30)
        self.hair_dark = (40, 30, 20)
        self.hair_light = (80, 70, 60)
        self.eye_color = (30, 30, 30)
        self.lip_color = (80, 80, 160)
        self.clothes_color = (80, 100, 180)
        self.clothes_secondary = (180, 180, 200)
        
        # === 面部关键点 (normalized 0-1) ===
        # 这些是 MediaPipe 478 点网格中提取的关键索引
        # 格式: (x, y) 归一化坐标，x=0左 y=0上
        self.landmarks = {}  # {name: (x, y)} 或 None
        
        # === 面部比例 ===
        self.face_w = 0.0     # 脸宽
        self.face_h = 0.0     # 脸高（前额到下巴）
        self.face_aspect = 1.0  # 宽高比
        self.eye_distance = 0.0  # 眼间距
        self.eye_to_mouth = 0.0  # 眼到嘴距离
        
    def is_valid(self):
        return self.has_face


# ====== MediaPipe 面部特征提取 ======
_FACE_LANDMARKER = None

def _get_landmarker():
    global _FACE_LANDMARKER
    if _FACE_LANDMARKER is not None:
        return _FACE_LANDMARKER
    if not _HAS_MEDIAPIPE:
        return None
    try:
        model_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "models", "face_landmarker.task"
        )
        if not os.path.exists(model_path):
            alt_path = os.path.expanduser("~/.hermes/models/face_landmarker.task")
            if os.path.exists(alt_path):
                model_path = alt_path
            else:
                print("[WARN] face_landmarker.task not found, downloading...")
                import urllib.request
                os.makedirs(os.path.dirname(model_path), exist_ok=True)
                url = "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task"
                urllib.request.urlretrieve(url, model_path)
                print(f"[OK] Downloaded to {model_path}")
        
        options = FaceLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=model_path),
            running_mode=RunningMode.IMAGE,
            min_face_detection_confidence=0.5
        )
        _FACE_LANDMARKER = FaceLandmarker.create_from_options(options)
        print("[OK] MediaPipe FaceLandmarker initialized")
        return _FACE_LANDMARKER
    except Exception as e:
        print(f"[WARN] Failed to init MediaPipe: {e}")
        return None


def extract_face_features_mediapipe(img):
    """使用MediaPipe FaceMesh提取478点面部特征"""
    if not _HAS_MEDIAPIPE:
        return None
    
    landmarker = _get_landmarker()
    if landmarker is None:
        return None
    
    try:
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w = img.shape[:2]
        mp_image = Image(image_format=ImageFormat.SRGB, data=rgb)
        result = landmarker.detect(mp_image)
        
        if not result.face_landmarks:
            return None
        
        mp_landmarks = result.face_landmarks[0]
        features = FaceFeatures()
        features.has_face = True
        features.mediapipe_detected = True
        
        # Store all 478 landmarks
        features.mp_landmarks = [(lm.x, lm.y, lm.z) for lm in mp_landmarks]
        
        # Extract face bounding box
        xs = [lm.x for lm in mp_landmarks]
        ys = [lm.y for lm in mp_landmarks]
        features.face_w = max(xs) - min(xs)
        features.face_h = max(ys) - min(ys)
        features.face_aspect = features.face_w / features.face_h if features.face_h > 0 else 1.0
        
        # --- Named landmarks (MediaPipe indices) ---
        key_indices = {
            # Face contour
            "forehead": 10,
            "chin": 152,
            "left_jaw": 172, "right_jaw": 397,
            "left_jaw_low": 136, "right_jaw_low": 365,
            "left_cheek": 234, "right_cheek": 454,
            # Eyes
            "left_eye_outer": 33, "left_eye_inner": 133,
            "left_eye_top": 159, "left_eye_bottom": 145,
            "right_eye_outer": 362, "right_eye_inner": 263,
            "right_eye_top": 386, "right_eye_bottom": 374,
            "left_iris": 468, "right_iris": 473,
            # Nose
            "nose_tip": 1, "nose_bridge": 168,
            "nose_bottom": 2, "nose_left": 49, "nose_right": 279,
            # Mouth
            "mouth_left": 61, "mouth_right": 291,
            "mouth_top": 13, "mouth_bottom": 14,
            # Eyebrows
            "left_brow_left": 46, "left_brow_right": 105,
            "right_brow_left": 334, "right_brow_right": 276,
        }
        for name, idx in key_indices.items():
            if idx < len(mp_landmarks):
                lm = mp_landmarks[idx]
                features.landmarks[name] = (lm.x, lm.y)
        
        # --- Compute derived measurements ---
        le = mp_landmarks[33]; re = mp_landmarks[362]
        features.eye_distance = re.x - le.x
        features.eye_to_mouth = mp_landmarks[13].y - (le.y + re.y) / 2
        
        # --- Extract colors (same as before but with better regions) ---
        features.skin_color = _extract_skin_color(img, mp_landmarks, w, h)
        features.hair_color, features.hair_dark, features.hair_light = _extract_hair_color(img, mp_landmarks, w, h)
        features.eye_color = _extract_eye_color(img, mp_landmarks, w, h)
        features.lip_color = _extract_lip_color(img, mp_landmarks, w, h)
        features.clothes_color, features.clothes_secondary = _extract_clothes_color(img, mp_landmarks, w, h)
        
        return features
        
    except Exception as e:
        print(f"[WARN] MediaPipe extraction error: {e}")
        return None


def _extract_skin_color(img, landmarks, w, h):
    """从脸颊区域提取皮肤颜色"""
    try:
        # Left cheek area
        lc = landmarks[234]
        rx, ry = int(lc.x * w), int(lc.y * h)
        size = max(5, int(w * 0.02))
        x1 = max(0, rx-size); x2 = min(w, rx+size)
        y1 = max(0, ry-size); y2 = min(h, ry+size)
        region = img[y1:y2, x1:x2]
        if region.size > 0:
            return tuple(np.median(region, axis=(0,1)).astype(int))
    except: pass
    return (200, 170, 150)


def _extract_hair_color(img, landmarks, w, h):
    """从头顶发际线区域提取头发颜色"""
    try:
        # Use forehead area and above
        forehead = landmarks[10]
        fy = int(forehead.y * h)
        fx = int(forehead.x * w)
        # Area above forehead
        hair_top = max(0, fy - int(h * 0.08))
        hair_bottom = max(0, fy - 2)
        hair_left = max(0, fx - int(w * 0.10))
        hair_right = min(w, fx + int(w * 0.10))
        if hair_bottom > hair_top and hair_right > hair_left:
            region = img[hair_top:hair_bottom, hair_left:hair_right]
            if region.size > 0:
                color = np.median(region, axis=(0,1)).astype(int)
                gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
                median_b = np.median(gray)
                _, dark_mask = cv2.threshold(gray, max(0, median_b-20), 255, cv2.THRESH_BINARY_INV)
                _, light_mask = cv2.threshold(gray, min(255, median_b+30), 255, cv2.THRESH_BINARY)
                dark_c = np.median(region[dark_mask>0], axis=0).astype(int) if np.sum(dark_mask>0)>10 else color
                light_c = np.median(region[light_mask>0], axis=0).astype(int) if np.sum(light_mask>0)>10 else np.clip(color*1.3, 0, 255).astype(int)
                return color, dark_c, light_c
    except: pass
    return (50, 40, 30), (40, 30, 20), (80, 70, 60)


def _extract_eye_color(img, landmarks, w, h):
    """从瞳孔位置提取眼睛颜色"""
    try:
        # Left iris area
        iris = landmarks[468]
        ix, iy = int(iris.x * w), int(iris.y * h)
        size = max(3, int(w * 0.01))
        x1 = max(0, ix-size); x2 = min(w, ix+size)
        y1 = max(0, iy-size); y2 = min(h, iy+size)
        region = img[y1:y2, x1:x2]
        if region.size > 0:
            gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
            _, dark = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY_INV)
            if np.sum(dark>0) > 3:
                return tuple(np.median(region[dark>0], axis=0).astype(int))
    except: pass
    return (30, 30, 30)


def _extract_lip_color(img, landmarks, w, h):
    """从嘴唇区域提取唇色"""
    try:
        mouth_top = landmarks[13]
        mouth_bottom = landmarks[14]
        mt = int(mouth_top.y * h)
        mb = int(mouth_bottom.y * h)
        ml = int(landmarks[61].x * w)
        mr = int(landmarks[291].x * w)
        if mb > mt and mr > ml:
            region = img[mt:mb, ml:mr]
            if region.size > 0:
                b, g, r = cv2.split(region)
                red_mask = (r > g + 10) & (r > b + 10)
                if np.sum(red_mask) > 5:
                    return tuple(np.median(region[red_mask], axis=0).astype(int))
                return tuple(np.median(region, axis=(0,1)).astype(int))
    except: pass
    return (80, 80, 160)


def _extract_clothes_color(img, landmarks, w, h):
    """从下巴以下的身体区域提取衣服颜色"""
    try:
        chin = landmarks[152]
        cy = int(chin.y * h) + 10
        body_h = int((chin.y - landmarks[10].y) * h * 0.4)
        cx = int(landmarks[152].x * w)
        body_left = max(0, cx - int(w * 0.12))
        body_right = min(w, cx + int(w * 0.12))
        if cy + body_h < h and body_right > body_left:
            region = img[cy:cy+body_h, body_left:body_right]
            if region.size > 0:
                pixels = region.reshape(-1, 3).astype(np.float32)
                criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
                _, labels, centers = cv2.kmeans(pixels, 3, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
                counts = np.bincount(labels.flatten())
                valid = []
                for i, c in enumerate(counts):
                    color = centers[i].astype(int)
                    brightness = np.mean(color)
                    if 30 < brightness < 240:
                        valid.append((c, color))
                if valid:
                    valid.sort(key=lambda x: -x[0])
                    main = tuple(valid[0][1])
                    sec = tuple(valid[1][1]) if len(valid) > 1 else main
                    return main, sec
    except: pass
    return (80, 100, 180), (180, 180, 200)


# ====== V3 Fallback (OpenCV Haar Cascade) ======
def extract_face_features_v3(img):
    """V3 fallback: use Haar Cascade (same as before)"""
    if cv2 is None:
        features = FaceFeatures()
        features.has_face = False
        return features
    
    features = FaceFeatures()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(80,80))
    
    if len(faces) == 0:
        return features
    
    x, y, fw, fh = max(faces, key=lambda r: r[2]*r[3])
    features.has_face = True
    features.face_w = fw
    features.face_h = fh
    features.face_aspect = fw/fh
    
    # Store basic landmarks for rendering
    h_img, w_img = img.shape[:2]
    features.landmarks["forehead"] = ((x+fw//2)/w_img, y/w_img)
    features.landmarks["chin"] = ((x+fw//2)/w_img, (y+fh)/w_img)
    features.landmarks["left_eye_outer"] = ((x+fw*0.25)/w_img, (y+fh*0.28)/w_img)
    features.landmarks["right_eye_outer"] = ((x+fw*0.75)/w_img, (y+fh*0.28)/w_img)
    features.landmarks["left_eye_inner"] = ((x+fw*0.38)/w_img, (y+fh*0.30)/w_img)
    features.landmarks["right_eye_inner"] = ((x+fw*0.62)/w_img, (y+fh*0.30)/w_img)
    features.landmarks["nose_tip"] = ((x+fw//2)/w_img, (y+fh*0.55)/w_img)
    features.landmarks["mouth_left"] = ((x+fw*0.30)/w_img, (y+fh*0.62)/w_img)
    features.landmarks["mouth_right"] = ((x+fw*0.70)/w_img, (y+fh*0.62)/w_img)
    features.landmarks["mouth_top"] = ((x+fw//2)/w_img, (y+fh*0.60)/w_img)
    features.landmarks["mouth_bottom"] = ((x+fw//2)/w_img, (y+fh*0.66)/w_img)
    features.landmarks["nose_bridge"] = ((x+fw//2)/w_img, (y+fh*0.38)/w_img)
    features.landmarks["left_jaw"] = ((x+fw*0.15)/w_img, (y+fh*0.55)/w_img)
    features.landmarks["right_jaw"] = ((x+fw*0.85)/w_img, (y+fh*0.55)/w_img)
    
    # Colors (simple version)
    features.skin_color = _extract_skin_color_simple(img, x, y, fw, fh)
    features.hair_color, features.hair_dark, features.hair_light = _extract_hair_color_simple(img, x, y, fw, fh)
    features.lip_color = _extract_lip_color_simple(img, x, y, fw, fh)
    
    return features

def _extract_skin_color_simple(img, x, y, fw, fh):
    cheek = img[y+int(fh*0.5):y+int(fh*0.7), x+int(fw*0.2):x+int(fw*0.8)]
    if cheek.size > 0:
        return tuple(np.clip(np.median(cheek, axis=(0,1)).astype(int) * 1.15, 0, 255).astype(int))
    return (200,170,150)

def _extract_hair_color_simple(img, x, y, fw, fh):
    h_img, w_img = img.shape[:2]
    hair_y = max(0, y - int(fh*0.35))
    hair_end = max(0, y-5)
    hair_left = max(0, x+int(fw*0.10))
    hair_right = min(w_img, x+int(fw*0.90))
    if hair_end > hair_y and hair_right > hair_left:
        region = img[hair_y:hair_end, hair_left:hair_right]
        if region.size > 0:
            color = np.median(region, axis=(0,1)).astype(int)
            return color, np.clip(color*0.8,0,255).astype(int), np.clip(color*1.3,0,255).astype(int)
    return (50,40,30), (40,30,20), (80,70,60)

def _extract_lip_color_simple(img, x, y, fw, fh):
    mouth = img[y+int(fh*0.55):y+int(fh*0.70), x+int(fw*0.25):x+int(fw*0.75)]
    if mouth.size > 0:
        b,g,r = cv2.split(mouth)
        red_mask = (r > g+10) & (r > b+10)
        if np.sum(red_mask) > 10:
            return tuple(np.median(mouth[red_mask], axis=0).astype(int))
    return (80,80,160)


# ====== 统一入口 ======
def extract_face_features(photo_path):
    """统一面部特征提取入口：MediaPipe优先，OpenCV回退"""
    if cv2 is None:
        print("[WARN] OpenCV not available, using default avatar")
        return FaceFeatures()
    
    img = cv2.imread(photo_path)
    if img is None:
        print(f"[WARN] Cannot load image: {photo_path}")
        return FaceFeatures()
    
    # Try MediaPipe first
    features = extract_face_features_mediapipe(img)
    if features is not None:
        print(f"[OK] MediaPipe FaceMesh detected!")
        return features
    
    # Fallback to OpenCV
    print("[INFO] MediaPipe unavailable, using OpenCV Haar fallback")
    return extract_face_features_v3(img)

# ====== Rendering Constants ======
# Canvas to head area mapping
HEAD_MARGIN_X = 10   # left/right margin
HEAD_MARGIN_Y = 5    # top margin
HEAD_BOTTOM_MARGIN = 30  # bottom margin (for body)

class QAvatarRenderer:
    """基于MediaPipe FaceMesh的V4版Q版渲染器"""
    
    def __init__(self, features: FaceFeatures):
        self.features = features
        self._last_params = Live2DParams()
    
    def render(self, canvas_size=(250, 250), params: Live2DParams = None) -> QPixmap:
        if params is None:
            params = Live2DParams()
        self._last_params = params
        
        cw, ch = canvas_size
        head_w = cw - HEAD_MARGIN_X * 2
        head_h = ch - HEAD_MARGIN_Y - HEAD_BOTTOM_MARGIN
        head_x0 = HEAD_MARGIN_X
        head_y0 = HEAD_MARGIN_Y
        
        pix = QPixmap(cw, ch)
        pix.fill(Qt.transparent)
        painter = QPainter(pix)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # ---- Breathing effect (global scale) ----
        breath = 1.0 + params.breath_amplitude * math.sin(params.breath_phase)
        body_sway = 2.0 * math.sin(params.body_sway_phase)
        
        # ---- Face-to-canvas mapping function ----
        ft = self.features
        if ft.mediapipe_detected:
            # Compute face bbox from landmarks
            xs = [ft.landmarks[n][0] for n in ["left_cheek","right_cheek","left_jaw","right_jaw","forehead","chin"]]
            ys = [ft.landmarks[n][1] for n in ["forehead","chin","left_jaw","right_jaw","left_cheek","right_cheek"]]
            face_min_x = min(xs)
            face_max_x = max(xs)
            face_min_y = min(ys)
            face_max_y = max(ys)
        else:
            face_min_x = 0.25; face_max_x = 0.75
            face_min_y = 0.15; face_max_y = 0.55
        
        face_w = max(0.001, face_max_x - face_min_x)
        face_h = max(0.001, face_max_y - face_min_y)
        
        def map_x(lm_x):
            return int(head_x0 + (lm_x - face_min_x) / face_w * head_w)
        
        def map_y(lm_y):
            return int(head_y0 + (lm_y - face_min_y) / face_h * head_h)
        
        # Grab landmark if available
        def lm(name):
            return ft.landmarks.get(name, None)
        
        # ============ 1. DRAW BODY ============
        body_top = map_y(0.47) if ft.mediapipe_detected else int(ch * 0.65)
        self._draw_body(painter, cw, body_top, ch - body_top, ft, breath)
        
        # ============ 2. DRAW HEAD ============
        self._draw_face_shape(painter, map_x, map_y, ft, lm, head_w, head_h)
        
        # ============ 3. DRAW HAIR (back layer) ============
        self._draw_hair_back(painter, map_x, map_y, ft, lm, params, head_w)
        
        # ============ 4. DRAW EYEBROWS ============
        self._draw_eyebrows(painter, map_x, map_y, ft, lm, params, head_w)
        
        # ============ 5. DRAW EYES ============
        self._draw_eyes(painter, map_x, map_y, ft, lm, params, head_w)
        
        # ============ 6. DRAW NOSE ============
        self._draw_nose(painter, map_x, map_y, ft, lm, head_w)
        
        # ============ 7. DRAW MOUTH ============
        self._draw_mouth(painter, map_x, map_y, ft, lm, params)
        
        # ============ 8. DRAW BLUSH ============
        self._draw_blush(painter, map_x, map_y, ft, lm, params)
        
        # ============ 9. DRAW HAIR (front) ============
        self._draw_hair_front(painter, map_x, map_y, ft, lm, params, head_w)
        
        painter.end()
        return pix
    
    # ---- Face shape ----
    def _draw_face_shape(self, painter, mx, my, ft, lm, hw, hh):
        """Draw face contour based on landmarks"""
        skin = ft.skin_color
        skin_q = QColor(int(skin[2]), int(skin[1]), int(skin[0]))
        
        if ft.mediapipe_detected and lm("chin") and lm("left_jaw") and lm("right_jaw"):
            # Use actual face contour: create QPainterPath from landmarks
            chin = lm("chin"); ljaw = lm("left_jaw"); rjaw = lm("right_jaw")
            forehead = lm("forehead"); lcheek = lm("left_cheek"); rcheek = lm("right_cheek")
            
            cx, cy = mx(chin[0]), my(chin[1])
            lx, ly = mx(ljaw[0]), my(ljaw[1])
            rx, ry = mx(rjaw[0]), my(rjaw[1])
            fx, fy = mx(forehead[0]), my(forehead[1])
            lcx, lcy = mx(lcheek[0]), my(lcheek[1])
            rcx, rcy = mx(rcheek[0]), my(rcheek[1])
            
            # Q版化调整：让脸更圆润（压缩左右宽度？或保持）
            # Build a smooth face contour
            path = QPainterPath()
            
            # Start at forehead center
            path.moveTo(fx, fy)
            
            # Left side: smooth curve through cheek to jaw to chin
            path.cubicTo(
                lcx, lcy,   # through left cheek
                lx, ly,     # to left jaw
                cx, cy      # to chin
            )
            
            # chin -> right jaw -> right cheek -> forehead
            path.cubicTo(
                rx, ry,     # through right jaw
                rcx, rcy,   # through right cheek
                fx, fy      # back to forehead
            )
            
            # Path auto-closed back to forehead
            painter.setBrush(QBrush(skin_q))
            painter.setPen(QPen(QColor(int(skin[2]*0.8), int(skin[1]*0.8), int(skin[0]*0.8)), 2))
            painter.drawPath(path)
        else:
            # Fallback: ellipse
            w = hw * 0.85
            h = hh * 0.90
            cx = mx(0.45)  # center-ish
            cy = my(0.30)
            r = QRect(cx - w//2, cy - h//2, w, h)
            painter.setBrush(QBrush(skin_q))
            painter.setPen(QPen(QColor(int(skin[2]*0.8), int(skin[1]*0.8), int(skin[0]*0.8)), 2))
            painter.drawEllipse(r)
    
    # ---- Eyes ----
    def _draw_eyes(self, painter, mx, my, ft, lm, params, hw):
        eye_color = ft.eye_color
        blink = params.eye_open
        look_x = int(params.eye_direction_x * 3)
        look_y = int(params.eye_direction_y * 2)
        
        if ft.mediapipe_detected and lm("left_eye_outer"):
            # ===== LANDMARK-BASED EYES =====
            left_outer = lm("left_eye_outer"); left_inner = lm("left_eye_inner")
            left_top = lm("left_eye_top"); left_bottom = lm("left_eye_bottom")
            right_outer = lm("right_eye_outer"); right_inner = lm("right_eye_inner")
            right_top = lm("right_eye_top"); right_bottom = lm("right_eye_bottom")
            left_iris = lm("left_iris"); right_iris = lm("right_iris")
            
            for side in ["left", "right"]:
                if side == "left":
                    outer = left_outer; inner = left_inner
                    top = left_top; bottom = left_bottom
                    iris = left_iris
                else:
                    outer = right_outer; inner = right_inner
                    top = right_top; bottom = right_bottom
                    iris = right_iris
                
                ox, oy = mx(outer[0]), my(outer[1])
                ix, iy = mx(inner[0]), my(inner[1])
                tx, ty = mx(top[0]), my(top[1])
                bx, by = mx(bottom[0]), my(bottom[1])
                
                eye_w = ix - ox
                eye_h = max(4, by - ty)
                cx = (ox + ix) // 2
                cy = (ty + by) // 2
                
                # Q版放大眼睛
                scale = 1.3
                q_eye_w = int(eye_w * scale)
                q_eye_h = max(4, int(eye_h * scale * blink))
                
                if blink > 0.15:
                    # Eye white
                    painter.setBrush(QBrush(Qt.white))
                    painter.setPen(QPen(QColor(60, 60, 60), 2))
                    painter.drawEllipse(cx - q_eye_w//2, cy - q_eye_h//2, q_eye_w, q_eye_h)
                    
                    # Iris
                    iris_r = max(3, q_eye_w // 3)
                    iris_r = int(iris_r * (0.6 + blink * 0.4))
                    icx = cx + look_x
                    icy = cy + look_y
                    
                    painter.setBrush(QBrush(QColor(
                        min(int(eye_color[2])+20, 255),
                        min(int(eye_color[1])+20, 255),
                        min(int(eye_color[0])+20, 255)
                    )))
                    painter.setPen(Qt.NoPen)
                    painter.drawEllipse(icx - iris_r, icy - iris_r, iris_r*2, iris_r*2)
                    
                    # Highlight
                    hl_r = max(2, iris_r - 2)
                    painter.setBrush(QBrush(Qt.white))
                    painter.drawEllipse(icx - hl_r//2 + look_x, icy - hl_r//2 - 1 + look_y, hl_r, hl_r)
                    
                    # 2nd highlight
                    painter.setBrush(QBrush(QColor(255, 255, 255, 120)))
                    painter.drawEllipse(icx + iris_r//4 + look_x, icy + iris_r//4 + look_y, 3, 3)
                else:
                    # Closed eye
                    painter.setPen(QPen(QColor(60, 40, 30), 2))
                    painter.drawLine(cx - q_eye_w//2, cy, cx + q_eye_w//2, cy)
        else:
            # Fallback: simple eyes
            self._draw_eyes_fallback(painter, mx, my, ft, params, hw)
    
    def _draw_eyes_fallback(self, painter, mx, my, ft, params, hw):
        eye_color = ft.eye_color
        blink = params.eye_open
        eye_y = my(0.35)
        eye_size_w = int(hw * 0.12)
        eye_size_h = int(hw * 0.10)
        cx = mx(0.45)
        spacing = int(hw * 0.14)
        
        cur_h = max(1, int(eye_size_h * blink))
        
        for sign in [-1, 1]:
            ecx = cx + sign * spacing
            if blink > 0.15:
                painter.setBrush(QBrush(Qt.white))
                painter.setPen(QPen(QColor(60,60,60), 2))
                painter.drawEllipse(ecx - eye_size_w//2, eye_y - cur_h//2, eye_size_w, cur_h)
                pupil_r = max(2, eye_size_w//3)
                eye_cx = ecx
                painter.setBrush(QBrush(QColor(eye_color[2], eye_color[1], eye_color[0])))
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(eye_cx - pupil_r, eye_y - pupil_r, pupil_r*2, pupil_r*2)
            else:
                painter.setPen(QPen(QColor(60,40,30), 2))
                painter.drawLine(ecx - eye_size_w//2, eye_y, ecx + eye_size_w//2, eye_y)
    
    # ---- Eyebrows ----
    def _draw_eyebrows(self, painter, mx, my, ft, lm, params, hw):
        raise_amt = params.brow_raise * 5 - params.anger * 3 + params.surprise * 6
        
        if ft.mediapipe_detected and lm("left_brow_left"):
            for side in ["left", "right"]:
                if side == "left":
                    bl = lm("left_brow_left"); br = lm("left_brow_right")
                else:
                    bl = lm("right_brow_left"); br = lm("right_brow_right")
                
                x1, y1 = mx(bl[0]), my(bl[1])
                x2, y2 = mx(br[0]), my(br[1])
                y_offset = int(raise_amt)
                
                painter.setPen(QPen(QColor(60, 40, 30), 2))
                painter.setBrush(Qt.NoBrush)
                path = QPainterPath()
                path.moveTo(x1, y1 + y_offset)
                path.cubicTo(
                    x1 + (x2-x1)//3, y1 + y_offset - 2,
                    x1 + (x2-x1)*2//3, y1 + y_offset + 1,
                    x2, y2 + y_offset + 2
                )
                painter.drawPath(path)
        else:
            brow_y = my(0.32)
            brow_w = int(hw * 0.10)
            cx = mx(0.45)
            spacing = int(hw * 0.14)
            for sign in [-1, 1]:
                bx = cx + sign * spacing
                painter.setPen(QPen(QColor(60, 40, 30), 2))
                painter.drawLine(bx - brow_w, brow_y, bx + brow_w, brow_y)
    
    # ---- Nose ----
    def _draw_nose(self, painter, mx, my, ft, lm, hw):
        if ft.mediapipe_detected and lm("nose_tip") and lm("nose_bridge"):
            tip = lm("nose_tip")
            bridge = lm("nose_bridge")
            nleft = lm("nose_left")
            nright = lm("nose_right")
            
            tx, ty = mx(tip[0]), my(tip[1])
            bx, by = mx(bridge[0]), my(bridge[1])
            lx, ly = mx(nleft[0]), my(nleft[1])
            rx, ry = mx(nright[0]), my(nright[1])
            
            # Q版鼻子: small cute nose
            painter.setPen(QPen(QColor(180, 150, 130), 2))
            painter.setBrush(Qt.NoBrush)
            
            # Simple dot nose
            navg_x = (lx + rx) // 2
            navg_y = (ty + by) // 2 + 5
            painter.drawEllipse(navg_x - 3, navg_y - 2, 6, 4)
        else:
            cx = mx(0.45)
            ny = my(0.45)
            painter.setPen(QPen(QColor(180, 150, 130), 2))
            painter.drawLine(cx, ny - 5, cx, ny + 3)
    
    # ---- Mouth ----
    def _draw_mouth(self, painter, mx, my, ft, lm, params):
        lip = ft.lip_color
        mouth_open = params.mouth_open
        happiness = params.happiness
        surprise = params.surprise
        
        if ft.mediapipe_detected and lm("mouth_left"):
            left = lm("mouth_left"); right = lm("mouth_right")
            top = lm("mouth_top"); bottom = lm("mouth_bottom")
            
            lx, ly = mx(left[0]), my(left[1])
            rx, ry = mx(right[0]), my(right[1])
            tx, ty = mx(top[0]), my(top[1])
            bx, by = mx(bottom[0]), my(bottom[1])
            
            cx = (lx + rx) // 2
            mouth_w = rx - lx
            mouth_h = max(3, by - ty)
            
            # Q版放大嘴
            scale = 1.2
            qw = int(mouth_w * scale)
            qh = max(3, int(mouth_h * scale))
            
            if mouth_open > 0.1 or surprise > 0.5:
                open_amt = max(mouth_open, surprise * 0.8)
                mh = int(qh * open_amt * 3)
                
                painter.setBrush(QBrush(QColor(
                    min(int(lip[2])+30, 255), min(int(lip[1])+20, 255), min(int(lip[0])+20, 255)
                )))
                painter.setPen(QPen(QColor(int(lip[2]), int(lip[1]), int(lip[0])), 1))
                painter.drawEllipse(cx - qw//2, by - mh//2, qw, mh)
                
                if mh > 4:
                    painter.setBrush(QBrush(QColor(60, 20, 20)))
                    painter.setPen(Qt.NoPen)
                    painter.drawEllipse(cx - qw//2 + 2, by - mh//2 + 1, qw - 4, mh - 2)
            else:
                # Smile arc
                smile_arc = int(60 + happiness * 60)
                painter.setPen(QPen(QColor(int(lip[2]), int(lip[1]), int(lip[0])), 2))
                painter.setBrush(Qt.NoBrush)
                painter.drawArc(cx - qw//2, by - qh,
                              qw, qh * 2,
                              0, smile_arc * 16)
        else:
            # Fallback
            lip_r, lip_g, lip_b = int(lip[2]), int(lip[1]), int(lip[0])
            cx = mx(0.45)
            mw = int(0.12 * mx(0.45))
            
            if mouth_open > 0.1:
                mh = int(mw * 0.6 * mouth_open * 3)
                painter.setBrush(QBrush(QColor(lip_r+30, lip_g+20, lip_b+20)))
                painter.setPen(QPen(QColor(lip_r, lip_g, lip_b), 1))
                painter.drawEllipse(cx - mw//2, mx(0.55) - mh//2, mw, mh)
            else:
                smile = int(60 + happiness * 60)
                painter.setPen(QPen(QColor(lip_r, lip_g, lip_b), 2))
                painter.setBrush(Qt.NoBrush)
                painter.drawArc(cx - mw, my(0.55), mw*2, int(mw*0.5), 0, smile*16)
    
    # ---- Blush ----
    def _draw_blush(self, painter, mx, my, ft, lm, params):
        intensity = min(80, int(60 + params.happiness * 40))
        
        if ft.mediapipe_detected and lm("left_cheek") and lm("right_cheek"):
            lc = lm("left_cheek"); rc = lm("right_cheek")
            chin = lm("chin"); forehead = lm("forehead")
            
            hh = my(chin[1]) - my(forehead[1])
            blush_r = max(3, int(hh * 0.06))
            
            painter.setBrush(QBrush(QColor(255, 150, 150, intensity)))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(mx(lc[0]) - blush_r, my(lc[1]) - blush_r//2, blush_r*2, blush_r)
            painter.drawEllipse(mx(rc[0]) - blush_r, my(rc[1]) - blush_r//2, blush_r*2, blush_r)
        else:
            cx = mx(0.45)
            blush_y = my(0.45)
            blush_r = int(0.05 * mx(0.45))
            spacing = int(0.14 * mx(0.45))
            painter.setBrush(QBrush(QColor(255, 150, 150, intensity)))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(cx - spacing - blush_r, blush_y - blush_r//2, blush_r*2, blush_r)
            painter.drawEllipse(cx + spacing - blush_r, blush_y - blush_r//2, blush_r*2, blush_r)
    
    # ---- Hair back layer ----
    def _draw_hair_back(self, painter, mx, my, ft, lm, params, hw):
        hair = ft.hair_color
        hair_dark = ft.hair_dark
        hair_color = QColor(int(hair[2]), int(hair[1]), int(hair[0]))
        hair_dark_c = QColor(int(hair_dark[2]), int(hair_dark[1]), int(hair_dark[0]))
        wave = params.hair_wave_phase
        
        if ft.mediapipe_detected and lm("forehead"):
            forehead = lm("forehead")
            chin = lm("chin"); ljaw = lm("left_jaw"); rjaw = lm("right_jaw")
            
            fx, fy = mx(forehead[0]), my(forehead[1])
            cx, cy = mx(chin[0]), my(chin[1])
            hh = cy - fy
            hw2 = hw * 0.5
            
            sway = int(5 * math.sin(wave))
            
            # Back hair volume (compact, just behind the head)
            path = QPainterPath()
            hair_r = int(hw2 * 0.70)
            path.addEllipse(fx - hair_r, fy - int(hh * 0.20), hair_r * 2, int(hh * 0.55))
            painter.setBrush(QBrush(hair_dark_c))
            painter.setPen(Qt.NoPen)
            painter.drawPath(path)
        else:
            # Fallback hair
            fx = mx(0.45); fy = my(0.20)
            r = mx(0.75); hair_r = (r - fx) * 1.3
            painter.setBrush(QBrush(hair_dark_c))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(fx - hair_r, fy - int(hair_r * 0.4), int(hair_r * 2), int(hair_r * 0.8))
    
    # ---- Hair front layer ----
    def _draw_hair_front(self, painter, mx, my, ft, lm, params, hw):
        hair = ft.hair_color
        hair_light = ft.hair_light
        hair_color = QColor(int(hair[2]), int(hair[1]), int(hair[0]))
        hair_light_c = QColor(int(hair_light[2]), int(hair_light[1]), int(hair_light[0]))
        wave = params.hair_wave_phase
        
        if ft.mediapipe_detected and lm("forehead"):
            forehead = lm("forehead")
            left_brow_l = lm("left_brow_left"); right_brow_r = lm("right_brow_right")
            
            fx, fy = mx(forehead[0]), my(forehead[1])
            chin = lm("chin"); cx, cy = mx(chin[0]), my(chin[1])
            hh = cy - fy
            hw2 = int(hw * 0.50)
            sway = int(5 * math.sin(wave))
            head_top_y = fy - int(hh * 0.15)
            
            # Main hair (top only, doesn't cover face)
            path = QPainterPath()
            hair_r = int(hw2 * 0.65)
            path.addEllipse(fx - hair_r, head_top_y, hair_r * 2, int(hh * 0.32))
            
            # Fill with main hair color
            painter.setBrush(QBrush(hair_color))
            painter.setPen(Qt.NoPen)
            painter.drawPath(path)
            
            # Fringe (bangs)
            brow_y = int((lm("left_brow_left")[1] + lm("left_brow_right")[1]) / 2)
            brow_canvas_y = my(brow_y)
            bangs_start_y = fy
            bangs_count = 8
            
            for i in range(bangs_count):
                px = fx - hw2 + int(i * hw2 * 2 / bangs_count) + sway
                py = bangs_start_y
                end_y = brow_canvas_y + int(hh * 0.08 * (i % 3) / 2)
                ratio = i / max(1, bangs_count - 1)
                r = int(hair[2] * (1-ratio) + hair_light[2] * ratio)
                g = int(hair[1] * (1-ratio) + hair_light[1] * ratio)
                b = int(hair[0] * (1-ratio) + hair_light[0] * ratio)
                
                painter.setPen(QPen(QColor(min(r,255), min(g,255), min(b,255)), 3 - (i % 2)))
                painter.setBrush(Qt.NoBrush)
                painter.drawLine(px, py, px, end_y)
        else:
            # Fallback: simple hair cap
            fx = mx(0.45); fy = my(0.20)
            r = mx(0.75); hair_r = (r - fx) * 1.2
            painter.setBrush(QBrush(hair_color))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(fx - hair_r, fy - int(hair_r * 1.2), int(hair_r * 2), int(hair_r * 1.5))
    
    # ---- Body ----
    def _draw_body(self, painter, cw, top, height, ft, breath):
        clothes = ft.clothes_color
        clothes2 = ft.clothes_secondary
        
        main_c = QColor(int(clothes[2]), int(clothes[1]), int(clothes[0]))
        acc_c = QColor(int(clothes2[2]), int(clothes2[1]), int(clothes2[0]))
        
        cx = cw // 2
        bw = int(cw * 0.30 * breath)
        
        # Small body (just shoulders/neck)
        path = QPainterPath()
        neck_w = max(8, bw // 2)
        path.moveTo(cx, top)
        path.cubicTo(
            cx - neck_w, top + height * 0.2,
            cx - bw, top + height * 0.4,
            cx - bw, top + height
        )
        path.lineTo(cx + bw, top + height)
        path.cubicTo(
            cx + bw, top + height * 0.4,
            cx + neck_w, top + height * 0.2,
            cx, top
        )
        
        painter.setBrush(QBrush(main_c))
        painter.setPen(QPen(acc_c, 1))
        painter.drawPath(path)
        
        # Collar
        collar_h = max(3, height // 4)
        painter.setBrush(QBrush(acc_c))
        painter.setPen(Qt.NoPen)
        col_path = QPainterPath()
        col_path.moveTo(cx - int(bw * 0.5), top)
        col_path.cubicTo(
            cx - int(bw * 0.3), top + collar_h,
            cx + int(bw * 0.3), top + collar_h,
            cx + int(bw * 0.5), top
        )
        painter.drawPath(col_path)


# ====== Live2D风格动画帧生成器 ======
class Live2DAnimator:
    def __init__(self, renderer: QAvatarRenderer, canvas_size=(250, 250)):
        self.renderer = renderer
        self.canvas_size = canvas_size
        self.params = Live2DParams()
        self.frame_count = 0
        self.blink_counter = 0
        self.next_blink = random.randint(90, 200)  # ~3-7 seconds at 30fps
    
    def update(self):
        """更新动画参数并渲染当前帧"""
        self.frame_count += 1
        p = self.params
        
        # 呼吸
        p.breath_phase += 0.05
        p.body_sway_phase += 0.02
        
        # 头发飘动
        p.hair_wave_phase += 0.08
        
        # 眨眼
        self.blink_counter += 1
        if self.blink_counter >= self.next_blink:
            # Start blinking sequence
            blink_frames = 6  # 6 frames to close and open
            if self.blink_counter - self.next_blink < blink_frames:
                t = (self.blink_counter - self.next_blink) / blink_frames
                if t < 0.5:
                    p.eye_open = 1.0 - (t * 2) * 0.9  # closing
                else:
                    p.eye_open = (t - 0.5) * 2 * 0.9  # opening
            else:
                p.eye_open = 1.0
                self.blink_counter = 0
                self.next_blink = random.randint(90, 200)
        
        # 情绪渐变（缓慢回归默认）
        p.happiness += (0.5 - p.happiness) * 0.01
        p.surprise *= 0.98
        p.anger *= 0.98
        
        return self.renderer.render(self.canvas_size, p)
    
    def set_mood(self, mood="normal"):
        """设置情绪状态"""
        p = self.params
        mood = mood.lower()
        if mood == "happy":
            p.happiness = 1.0; p.surprise = 0.0; p.anger = 0.0
        elif mood == "angry":
            p.happiness = 0.1; p.surprise = 0.0; p.anger = 0.8
        elif mood == "surprised":
            p.happiness = 0.3; p.surprise = 1.0; p.anger = 0.0
        elif mood == "sad":
            p.happiness = 0.0; p.surprise = 0.0; p.anger = 0.0


# ====== 用于测试的独立运行入口 ======
def test_render():
    """测试渲染输出（保存到文件）"""
    import sys
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Try to find a photo
    photo_path = "assets/images/jiejie.jpg"
    if not os.path.exists(photo_path):
        import glob
        photos = glob.glob("assets/images/*.jpg") + glob.glob("assets/images/*.png")
        if photos:
            photo_path = photos[0]
        else:
            print("No photo found")
            return
    
    print(f"[TEST] Extracting features from: {photo_path}")
    features = extract_face_features(photo_path)
    
    if not features or not features.has_face:
        print("[TEST] No face detected, using defaults")
        features = FaceFeatures()
    
    print(f"[TEST] Creating renderer (detected={'MediaPipe' if features.mediapipe_detected else 'OpenCV'})")
    renderer = QAvatarRenderer(features)
    animator = Live2DAnimator(renderer, canvas_size=(250, 250))
    
    # Render a few frames
    for i in range(10):
        pix = animator.update()
        if i == 0:
            pix.save("/tmp/avatar_v4_test.png")
            print(f"[TEST] Saved frame to /tmp/avatar_v4_test.png ({pix.width()}x{pix.height()})")
    
    print("[TEST] Done!")

if __name__ == "__main__":
    test_render()
