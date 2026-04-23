# 桌面宠物程序

## 📥 下载
**最新版本: v1.0.2**  

### 🪟 Windows用户（推荐）
- [DesktopPet.exe](https://github.com/luomodeshang/desktop-pet/releases/download/v1.0.2/DesktopPet.exe) - 单个可执行文件，双击即可运行
- [DesktopPet_Windows_v1.0.2.zip](https://github.com/luomodeshang/desktop-pet/releases/download/v1.0.2/DesktopPet_Windows_v1.0.2.zip) - 绿色免安装版
- [DesktopPet_Setup.exe](https://github.com/luomodeshang/desktop-pet/releases/download/v1.0.2/DesktopPet_Setup.exe) - 安装程序版

### 💻 开发者/高级用户
- [源代码包](https://github.com/luomodeshang/desktop-pet/releases/download/v1.0.2/desktop-pet-v1.0.2-source.tar.gz) - 完整源代码，需要Python环境

查看所有版本: [Releases页面](https://github.com/luomodeshang/desktop-pet/releases)

## 🎯 功能特性
- 使用你的照片生成动漫风格宠物
- 右键投喂（汉堡、炸鸡、螺蛳粉）
- 左键点击触发动作（挥手、跳跃、踱步）
- 闲置时自动切换状态（站立→蹲下→睡眠）
- 状态自动保存

## 使用方法
1. 安装依赖：`pip install -r requirements.txt`
2. 处理照片：`python process_photo_simple.py`
3. 启动程序：`python src/main.py`

## 文件结构
- `src/main.py` - 主程序
- `process_photo_simple.py` - 照片处理
- `assets/images/` - 图像资源
- `config/` - 配置文件

## 控制方式
- 左键点击：触发宠物动作
- 右键点击：显示投喂菜单
- 拖动：移动宠物位置
- 系统托盘：右键退出
