#!/usr/bin/env python3
"""
Desktop Pet - 桌面宠物
Using QAvatarRenderer + AnimationEngine
"""
import sys, os, json, random, math, shutil, traceback
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import *

# Fix import for "python src/main.py" (Windows cmd)
_script_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(_script_dir)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)
from src.qavatar_generator import extract_face_features, QAvatarRenderer, Live2DAnimator
from src.animation_engine import AnimationEngine, AnimationType, FrameGenerator

ASSETS_DIR = "assets"
CONFIG_DIR = "config"
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(CONFIG_DIR, exist_ok=True)
PHOTO_CACHE = os.path.join(IMAGES_DIR, "user_pet.png")
CONFIG_PATH = os.path.join(CONFIG_DIR, "pet_config.json")
DEFAULT_PHOTO = os.path.join(IMAGES_DIR, "jiejie.jpg")
JUMP_OFFSET = 80  # Extra window height so jump doesn't clip

class DesktopPet(QWidget):
    def __init__(self, photo_path=None):
        super().__init__()
        self.photo_path = photo_path
        self.pet_size_index = 3
        self.size_options = [100, 150, 200, 250, 300]
        self.pet_w = self.size_options[self.pet_size_index]
        self.pet_h = self.size_options[self.pet_size_index]
        self.is_dragging = False
        self.drag_position = QPoint()
        self.last_interaction = datetime.now()
        self.current_state = "standing"
        self._feeding_lock = False
        self._feed_cooldown_timer = QTimer(self)
        self._feed_cooldown_timer.setSingleShot(True)
        self.food_list = ["Burger", "Fried Chicken", "Snail Noodles"]
        self.food_colors = {"Burger": (255,180,50), "Fried Chicken": (220,150,80), "Snail Noodles": (200,150,80)}
        self.config = self.load_config()
        self.init_ui()
        self.renderer = None
        self.animator = None
        self.frame_generator = FrameGenerator(pet_size=(self.pet_w, self.pet_h))
        self.engine = AnimationEngine(frame_generator=self.frame_generator, on_render=self._on_render_callback)
        self._init_avatar()
        self.init_tray()
        self.state_timer = QTimer(self)
        self.state_timer.timeout.connect(self.check_state)
        self.state_timer.start(5000)
        self._history_action = None
        print("[OK] Desktop Pet started!")

    def init_ui(self):
        self.window_h = self.pet_h + JUMP_OFFSET
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(self.pet_w, self.window_h)
        screen = QApplication.primaryScreen().geometry()
        self.move(screen.width()-self.pet_w-40, screen.height()-self.window_h-80)
        self.setMouseTracking(True)

    def _init_avatar(self):
        if self.photo_path and os.path.exists(self.photo_path):
            self._create_from_photo(self.photo_path); return
        if os.path.exists(DEFAULT_PHOTO):
            self._create_from_photo(DEFAULT_PHOTO); return
        photo = self.config.get("user_photo")
        if photo and os.path.exists(photo):
            self._create_from_photo(photo); return
        if os.path.exists(PHOTO_CACHE):
            self._create_from_photo(PHOTO_CACHE); return
        self._create_default_avatar()

    def _create_from_photo(self, path):
        print(f"[INFO] Processing photo: {path}")
        f = extract_face_features(path)
        if f.has_face: print(f"[OK] Face detected! Shape: {f.face_shape}")
        else: print("[WARN] No face detected")
        self.renderer = QAvatarRenderer(f)
        self.animator = Live2DAnimator(self.renderer, canvas_size=(self.pet_w, self.pet_h))
        pix = self.renderer.render((self.pet_w, self.pet_h))
        self.frame_generator.set_base_image(pix)
        self.frame_generator._cache.clear()
        self.engine._ensure_cache(AnimationType.NONE)

    def _create_default_avatar(self):
        from src.qavatar_generator import FaceFeatures
        print("[INFO] Creating default avatar")
        f = FaceFeatures()
        f.has_face = False; f.skin_color = (200,170,150); f.hair_color = (50,40,30)
        f.eye_color = (30,30,30); f.lip_color = (80,80,160)
        f.clothes_color = (80,100,180); f.clothes_secondary = (180,180,200)
        f.face_shape = "round"
        self.renderer = QAvatarRenderer(f)
        self.animator = Live2DAnimator(self.renderer, canvas_size=(self.pet_w, self.pet_h))
        pix = self.renderer.render((self.pet_w, self.pet_h))
        self.frame_generator.set_base_image(pix)
        self.frame_generator._cache.clear()
        self.engine._ensure_cache(AnimationType.NONE)

    def init_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        # Use QAvatar as tray icon (resize render output to 32x32)
        ip = QPixmap(32,32); ip.fill(Qt.transparent)
        if self.renderer:
            rp = self.renderer.render((32,32))
            p = QPainter(ip); p.drawPixmap(0,0,rp); p.end()
        else:
            p = QPainter(ip)
            p.setBrush(QBrush(QColor(100,150,200,180)))
            p.setPen(Qt.NoPen); p.drawEllipse(2,2,28,28); p.end()
        self.tray_icon.setIcon(QIcon(ip)); self.tray_icon.show()
        tm = QMenu()
        sm = tm.addMenu("Size")
        labels = ["Small(100)","Medium(150)","Large(200)","XL(250)","XXL(300)"]
        self._size_actions = []
        for i,lbl in enumerate(labels):
            a = QAction(lbl,self); a.setCheckable(True); a.setChecked(i==self.pet_size_index)
            a.triggered.connect(lambda chk,idx=i: self.set_pet_size(idx))
            sm.addAction(a); self._size_actions.append(a)
        ca = QAction("Change Photo",self); ca.triggered.connect(self.change_photo); tm.addAction(ca)
        ha = QAction("Food History",self); ha.triggered.connect(self.show_food_history); tm.addAction(ha)
        tm.addSeparator()
        ea = QAction("Exit",self); ea.triggered.connect(self.quit_application); tm.addAction(ea)
        self.tray_icon.setContextMenu(tm)

    def set_pet_size(self, idx):
        if 0<=idx<len(self.size_options):
            self.pet_size_index=idx; self.pet_w=self.size_options[idx]; self.pet_h=self.size_options[idx]
            self.resize(self.pet_w,self.pet_h)
            if self.renderer:
                pix=self.renderer.render((self.pet_w,self.pet_h))
                self.frame_generator.set_base_image(pix); self.frame_generator.set_pet_size(self.pet_w,self.pet_h)
            for i,a in enumerate(self._size_actions): a.setChecked(i==idx)
            self.save_config()

    def change_photo(self):
        fp,_=QFileDialog.getOpenFileName(self,"Select Photo","","Images (*.jpg *.jpeg *.png *.bmp *.gif)")
        if fp:
            shutil.copy2(fp,PHOTO_CACHE)
            self._create_from_photo(PHOTO_CACHE)
            self.config["user_photo"]=fp; self.config["use_default_avatar"]=False; self.save_config()
            QMessageBox.information(self,"OK","Photo changed!")

    def show_food_history(self):
        h=self.config.get("food_history",[])
        if not h: QMessageBox.information(self,"Food History","No records yet"); return
        QMessageBox.information(self,"Food History","\n".join(["Food History:"]+[f"{x['time']} - {x['food']}" for x in h[-15:]]))

    def quit_application(self):
        self.save_config()
        if hasattr(self,'engine') and self.engine: self.engine.stop()
        QApplication.quit()

    def _on_render_callback(self,at,fi): self.update()

    def paintEvent(self,ev):
        p=QPainter(self); p.setRenderHint(QPainter.Antialiasing)
        fr=None
        if hasattr(self,'engine') and self.engine: fr=self.engine.get_current_frame()
        if fr is None and hasattr(self,'animator') and self.animator:
            fr=self.animator.update()
        if fr:
            pixmap = fr
            if pixmap.size().width() != self.pet_w or pixmap.size().height() != self.pet_h:
                pixmap = pixmap.scaled(self.pet_w, self.pet_h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            # Draw at bottom so jump has room above
            draw_y = self.window_h - pixmap.height()
            draw_x = (self.pet_w - pixmap.width()) // 2
            p.drawPixmap(draw_x, draw_y, pixmap)

    def mousePressEvent(self,ev):
        if ev.button()==Qt.LeftButton: self._trigger_action(); self.last_interaction=datetime.now()
        elif ev.button()==Qt.RightButton: self._show_feed_menu(ev.globalPos())
        self.is_dragging=True; self.drag_position=ev.globalPos()-self.frameGeometry().topLeft(); ev.accept()

    def mouseDoubleClickEvent(self,ev):
        if ev.button()==Qt.LeftButton: self._spin_jump(); ev.accept()

    def mouseMoveEvent(self,ev):
        if self.is_dragging and ev.buttons()&Qt.LeftButton: self.move(ev.globalPos()-self.drag_position); ev.accept()

    def mouseReleaseEvent(self,ev): self.is_dragging=False

    def _trigger_action(self):
        if not hasattr(self,'engine') or not self.engine: return
        if self._feeding_lock: return
        ch=random.choice(["wave","jump","walk"])
        self.last_interaction=datetime.now(); self.current_state="standing"
        self.engine.play({"wave":AnimationType.WAVE,"jump":AnimationType.JUMP,"walk":AnimationType.WALK}[ch])
        print(f"Action: {ch}")

    def _spin_jump(self):
        if not hasattr(self,'engine') or not self.engine: return
        self.engine.play(AnimationType.JUMP); print("Spin jump!")

    def _show_feed_menu(self,pos):
        if self._feeding_lock: return
        m=QMenu(self)
        for f in self.food_list:
            a=QAction(f,self); a.triggered.connect(lambda chk,fn=f: self._feed_with_trigger(fn)); m.addAction(a)
        m.exec_(pos)

    def _feed_with_trigger(self,fn): self._feed(fn)

    def _feed(self,fn):
        if not hasattr(self,'_feeding_lock'): self._feeding_lock=False
        if self._feeding_lock: print(f"[FEED] Still eating, ignoring {fn}"); return
        self._feeding_lock=True; self.last_interaction=datetime.now(); self.current_state="standing"
        print(f"[FEED] {fn}")
        if hasattr(self,'engine') and self.engine:
            self.engine.state.food_name=fn; self.engine.generator._feed_food_type=fn; self.engine.play(AnimationType.FEED)
        h=self.config.get("food_history",[])
        h.append({"food":fn,"time":datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        self.config["food_history"]=h; self.save_config()
        if not hasattr(self,'_feed_cooldown_timer') or self._feed_cooldown_timer is None:
            self._feed_cooldown_timer=QTimer(self); self._feed_cooldown_timer.setSingleShot(True)
        try: self._feed_cooldown_timer.timeout.disconnect()
        except TypeError: pass
        self._feed_cooldown_timer.timeout.connect(self._unlock_feed); self._feed_cooldown_timer.start(2500)

    def _unlock_feed(self): self._feeding_lock=False; print("[FEED] Ready")

    def check_state(self):
        it=(datetime.now()-self.last_interaction).total_seconds()
        if it>120:
            if self.current_state!="sleeping":
                self.current_state="sleeping"
                if self.animator and self.engine.state.anim_type==AnimationType.NONE:
                    self.animator.params.eye_open=0.0; self.animator.params.happiness=0.2
        elif it>30:
            if self.current_state!="crouching":
                self.current_state="crouching"
                if self.animator: self.animator.params.eye_open=0.6; self.animator.params.happiness=0.3
        else:
            if self.current_state not in ("standing",None):
                self.current_state="standing"
                if self.animator: self.animator.params.eye_open=1.0; self.animator.params.happiness=0.5

    def load_config(self):
        d={"pet_size_index":3,"position":[100,100],"last_state":"standing","food_history":[],"user_photo":None,"use_default_avatar":True}
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH,"r",encoding="utf-8") as f:
                    l=json.load(f)
                    for k in d:
                        if k not in l: l[k]=d[k]
                    return l
            except: pass
        return dict(d)

    def save_config(self):
        c={"pet_size_index":self.pet_size_index,"position":[self.x(),self.y()],"last_state":self.current_state,"food_history":self.config.get("food_history",[]),"user_photo":self.config.get("user_photo"),"use_default_avatar":self.config.get("use_default_avatar",True)}
        with open(CONFIG_PATH,"w",encoding="utf-8") as f: json.dump(c,f,ensure_ascii=False,indent=2)

    def closeEvent(self,ev):
        self.save_config()
        if hasattr(self,'engine'): self.engine.stop()
        ev.accept()

def main():
    try:
        print("="*40); print("  Desktop Pet"); print("="*40); print()
        app=QApplication(sys.argv); app.setQuitOnLastWindowClosed(False)
        pp=None
        if len(sys.argv)>1 and os.path.exists(sys.argv[1]): pp=sys.argv[1]
        pet=DesktopPet(pp); pet.show()
        print("Controls:"); print("- Left-click: Random action (wave/jump/walk)"); print("- Double-click: Spin jump!"); print("- Right-click: Feed food (burger/fries/snail noodles)"); print("- Drag: Move pet"); print("- Tray menu: Size/Photo/History/Exit"); print()
        print("Features:"); print("- Photo to Q-Avatar (chibi style)"); print("- Auto clothes color matching"); print("- Live2D style animation (breath/blink/hair wave)"); print("- Mood-driven expressions (happy/surprised/eating)"); print("- Idle states (stand/crouch/sleep)")
        sys.exit(app.exec_())
    except Exception as e:
        print(f"[ERROR] {e}"); import traceback; traceback.print_exc(); input("Press Enter to exit...")

if __name__=="__main__": main()
