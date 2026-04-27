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

| 版本 | 亮点 |
|------|------|
| **v3.0** | Q版小人生成 + Live2D风格动画 + 衣服颜色匹配 |
| v2.0 | 照片卡通化 + 完整交互逻辑 |
| v1.0 | 基础桌面宠物框架 |

---

*Made with ❤️ by luomodeshang*
