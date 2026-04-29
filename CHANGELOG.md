# 📋 更新日志

## v4.0.1 (2026-04-29)
### 🐛 修复
- **默认尺寸从 250px 改为 150px**：适配小屏幕，不再显示不全
- **修复 `face_shape` 属性错误**：V4版 `FaceFeatures` 无此属性，删除引用
- **修复头部与身体分离**：fallback模式下 `body_top` 位置从0.80改为0.65
- **补充 fallback 模式头发渲染**：OpenCV模式下也正常显示
- **修复 OpenCV 版本冲突**：自动检测并修复 `opencv-python` 与 `opencv-contrib-python` 冲突
- **修复 bat 脚本语法**：改用扁平 goto 结构，避免嵌套 if 解析失败

### ✨ 新增
- **自动安装 MediaPipe**：启动时自动 `pip install mediapipe`（仅首次）
- **内置离线 whl 包**：`deps/` 目录下自带 MediaPipe 安装包，断网也能装
- **自动下载模型**：首次运行自动下载 478 点面部网格模型
- **清华/阿里云镜像优先**：国内网络友好

### 🎮 体验
- 无编程基础用户也可直接双击 `run.bat` 运行
- 所有依赖自动安装，无需手动操作
- 支持 V4 完整渲染（MediaPipe）和 OpenCV 回退模式
