# Desktop Pet 🐾

> **v3.0 — Q版重生！从照片生成会呼吸眨眼的专属桌面宠物**

[![GitHub release](https://img.shields.io/github/v/release/luomodeshang/desktop-pet)](https://github.com/luomodeshang/desktop-pet/releases)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15%2B-green)](https://pypi.org/project/PyQt5/)

---

## ✨ 新特性 (v3.0)

| 特性 | 说明 |
|------|------|
| 🎨 **Q版小人生成** | 从你的照片自动生成大头小身体的Q版角色 |
| 👕 **衣服颜色匹配** | 自动提取照片中的衣服颜色，角色穿同色衣服 |
| 🌊 **Live2D风格动画** | 呼吸起伏、眨眼、头发飘动、视线移动 |
| 😊 **情绪表情系统** | 开心微笑、惊喜张嘴、吃东西咀嚼 |
| 🖱️ **双击旋转跳跃** | 双击宠物触发特殊动画 |
| 📏 **大小可调节** | 托盘菜单中调整宠物大小（100/150/200/250px） |

---

## 🚀 快速开始（Windows）

### 前提条件

安装 **Python 3.8+**（如果没有的话）：
- 下载：https://www.python.org/downloads/
- **安装时务必勾选** ☑️ "Add Python to PATH"
- 验证：打开命令提示符运行 `python --version`

### 一键启动

```batch
git clone https://github.com/luomodeshang/desktop-pet.git
cd desktop-pet
run.bat
```

> `run.bat` 会自动安装所需依赖（PyQt5、OpenCV、Pillow等），首次运行可能稍慢。

### 手动安装

```batch
pip install PyQt5 opencv-python pillow numpy
python src/main.py
```

---

## 🎮 使用方法

| 操作 | 效果 |
|------|------|
| **首次运行** | 弹出照片选择对话框，选一张照片，生成专属Q版角色 |
| **左键点击** | 随机动作（挥手/跳跃/踱步）+ 开心表情 |
| **双击** | 旋转跳跃！ |
| **右键点击** | 投喂菜单（汉堡/炸鸡/螺蛳粉）-> 咀嚼表情 |
| **拖拽** | 按住左键拖动到任意位置 |
| **托盘菜单** | 投喂 / 调整大小 / 更换照片 / 查看食物历史 / 退出 |

### 空闲状态

- 30秒无操作 -> 蹲下（半闭眼放松）
- 2分钟无操作 -> 睡眠（全闭眼）

---

## 📷 照片要求

为了获得最佳Q版效果，建议：
- 正面或半侧面人脸照片
- 光线充足，面部清晰可见
- 最好能拍到部分衣服/上半身
- 避免逆光、极度侧脸、多人合照

> 如果未检测到人脸，会自动回退到简单卡通模式。

---

## 📁 项目结构

```
desktop-pet/
├── src/
│   ├── main.py                  # 主程序入口
│   ├── qavatar_generator.py     # Q版角色生成器 + Live2D引擎
│   └── animation_engine.py      # 统一动画帧循环
├── assets/images/
│   └── icon.ico                 # 程序图标
├── run.bat                      # Windows一键启动
├── run.sh                       # Linux/Mac启动
├── requirements.txt             # Python依赖
├── CHANGELOG_v3.0.md            # v3.0更新说明
└── README.md
```

---

## 🛠️ 技术栈

| 组件 | 用途 |
|------|------|
| Python 3.8+ | 运行环境 |
| PyQt5 | GUI + 动画 |
| OpenCV | 人脸检测 + 颜色提取 |
| NumPy | 数学计算 |
| Pillow | 图像处理 |

---

## 📜 版本历史

| 版本 | 亮点 | 详细说明 |
|------|------|----------|
| **v3.0.13** | 窗口加高 + 喂食改进 + 挥手自然 | 窗体高度改为1.5倍，跳跃不会出界；三种食物不同食材图案+手部动作+去掉吃完表情；挥手改用弧形摆臂+身体微晃 |
| **v3.0.12** | 修复动画不刷新 | 回调中触发self.update()，动画帧能实时显示 |
| **v3.0.11** | 修复初始渲染 + 托盘图标 + 默认照片 | 修复打开时人物不显示（base_pixmap在初始化时为空）；托盘图标改为使用Q版头像；默认使用assets/images/jiejie.jpg |
| **v3.0.10** | 修复 random 导入错误 | qavatar_generator.py 缺失 import random 导致 Windows 下 NameError |
| **v3.0.9** | 修复 Windows 模块导入路径 | python src/main.py 运行时 from src.qavatar_generator 找不到模块；添加 sys.path 修正 |
| **v3.0.8** | import shutil 移至模块顶部 | change_photo() 方法内部的 import shutil 移到文件顶部 |
| **v3.0.7** | 修复JUMP/WALK动画 + 增强头像渲染 | JUMP 弹跳 60px + 压缩拉伸动画；WALK 左右摆动 + 上下颠簸；头发增强为渐变刘海 + 侧发双缕 |
| **v3.0.6** | 修复默认尺寸 + 喂食闪退 | 默认尺寸改为250px；右键触发改用 QAction 独立方法；头发重写三层贝塞尔+渐变刘海 |
| **v3.0.5** | 修复JUMP/WALK帧渲染 | 为_ensure_cache添加 JUMP/WALK prerender，防止 pet 消失 |
| **v3.0.4** | FrameGenerator init 顺序修复 | engine/frame_generator 在_init_avatar前创建，修复 AttributeError |
| **v3.0.3** | 增强头发渲染 | 增加头发细节，左右侧发，暗/亮两层上色 |
| **v3.0.2** | 修复喂食动画时间 | QTimer 从 1500ms 延长到 2500ms |
| **v3.0.1** | 默认尺寸 250px | pet_size_index 从 1 改为 3 |
| **v3.0** | Q版小人生成 + Live2D风格动画 + 衣服颜色匹配 | 从照片自动生成 Q 版角色，呼吸眨眼头发飘动，情绪表情系统 |
| v2.0 | 照片卡通化 + 完整交互逻辑 | OpenCV 滤镜 + 卡通化 + 喂食/动作/状态切换 |
| v1.0 | 基础桌面宠物框架 | 窗口拖拽 + 基础动画 + 托盘菜单 |

---

*Made with ❤️ by luomodeshang*