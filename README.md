# Desktop Pet 🐾

基于 PyQt5 的桌面宠物程序，使用您的照片生成动漫风格宠物。

## 功能

- 📸 **照片卡通化** — 上传照片生成卡通风格宠物
- 🍔 **右键投喂** — 汉堡、炸鸡、螺蛳粉
- 👋 **左键互动** — 挥手、跳跃、踱步
- 😴 **自动状态** — 站立 → 蹲下 → 睡眠
- 💾 **状态保存** — 自动保存配置

## 安装（Windows）

### 方法1：一键安装

1. 下载 [DesktopPet_Setup.bat](https://raw.githubusercontent.com/luomodeshang/desktop-pet/main/DesktopPet_Setup.bat)
2. 双击运行（会自动下载所有文件并安装依赖）
3. 耐心等待安装完成，桌面会出现「Desktop Pet」文件夹
4. 双击 `run.bat` 启动

### 方法2：手动安装

**前提：安装 Python 3.10+**

```
# 下载并解压项目
git clone https://github.com/luomodeshang/desktop-pet.git
cd desktop-pet

# 安装依赖
pip install PyQt5 opencv-python pillow numpy

# 运行
python src/main.py
```

## 使用方法

| 操作 | 说明 |
|------|------|
| **首次运行** | 弹出照片选择对话框 → 选择照片 → 自动生成卡通宠物 |
| **左键点击** | 随机触发挥手/跳跃/踱步动画 |
| **右键点击** | 显示投喂菜单 → 选择食物 |
| **拖拽** | 按住左键拖动宠物到任意位置 |
| **托盘右键** | 投喂、更换照片、查看食物历史、退出 |

## 技术栈

- Python 3.10+
- PyQt5
- OpenCV
- Pillow
- NumPy

## 项目结构

```
desktop-pet/
├── src/
│   ├── main.py              # 主程序
│   ├── icon_manager_gui.py  # 图标管理器
│   └── icon_manager.py      # 图标管理工具
├── assets/
│   └── images/
│       └── icon.ico         # 程序图标
├── run.bat                  # Windows运行脚本
├── run.sh                   # Linux/Mac运行脚本
├── requirements.txt         # Python依赖
└── README.md
```
