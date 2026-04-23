# 🐱 桌面宠物程序 - Windows版

**把你的照片变成会动的桌面宠物！支持喂食、互动、自动保存状态。**

## 📥 快速开始（小白专用）

### 方法一：一键安装（推荐）
1. **[点击下载安装程序](https://github.com/luomodeshang/desktop-pet/releases/latest/download/DesktopPet_Setup.exe)**
2. 双击运行 `DesktopPet_Setup.exe`
3. 下一步 → 下一步完成安装
4. 桌面出现宠物图标，双击运行

### 方法二：绿色免安装
1. **[点击下载绿色版](https://github.com/luomodeshang/desktop-pet/releases/latest/download/DesktopPet_Windows_v1.0.0.zip)**
2. 解压到任意文件夹
3. 双击 `DesktopPet.exe` 运行

> ⚠️ **注意**：如果Windows Defender或杀毒软件报警，请点击"允许"或"信任此程序"

## 🎮 功能特色

### 🖼️ 照片转动漫
- 选择任意照片，自动转换为动漫风格宠物
- 支持人脸识别，智能生成可爱形象
- 保留原照片特征，个性化定制

### 🍔 投喂互动
- **右键点击**投喂三种食物：
  - 🍔 汉堡
  - 🍗 炸鸡  
  - 🍜 螺蛳粉
- 宠物会有不同的吃食动画

### 👆 动作互动
- **左键点击**触发三种动作：
  - 👋 挥手
  - 🦘 跳跃
  - 🚶 踱步
- 宠物随机展示不同动作

### 💤 智能状态
- 自动切换状态：站立 → 蹲下 → 睡觉
- 长时间不动会自动睡觉
- 点击唤醒，恢复活力

### 💾 自动保存
- 退出时自动保存宠物状态
- 下次启动恢复位置和状态
- 支持多设备数据备份

## 🖥️ 系统要求

| 项目 | 最低要求 | 推荐配置 |
|------|----------|----------|
| **操作系统** | Windows 10 | Windows 11 |
| **处理器** | Intel i3 或同等 | Intel i5 或同等 |
| **内存** | 4 GB RAM | 8 GB RAM |
| **存储空间** | 200 MB 可用空间 | 500 MB 可用空间 |
| **显卡** | 集成显卡 | 独立显卡 |
| **屏幕分辨率** | 1366×768 | 1920×1080 |

## 🔧 安装说明

### 完整安装步骤
1. **下载安装程序**
   ```
   https://github.com/luomodeshang/desktop-pet/releases/latest
   ```

2. **运行安装向导**
   - 选择安装语言（中文/英文）
   - 选择安装目录（默认：`C:\Program Files\桌面宠物程序`）
   - 选择是否创建桌面快捷方式
   - 点击"安装"开始安装

3. **首次运行配置**
   - 启动程序，选择一张照片
   - 等待照片转换（约10-30秒）
   - 宠物出现在桌面右下角

### 静默安装（IT管理员）
```cmd
DesktopPet_Setup.exe /SILENT /NORESTART
```

参数说明：
- `/SILENT` - 静默安装，不显示界面
- `/NORESTART` - 安装后不重启
- `/DIR="C:\MyApp"` - 指定安装目录

## ⚙️ 配置说明

### 配置文件位置
```
C:\Users\<用户名>\AppData\Roaming\桌面宠物程序\data\
```

主要文件：
- `pet_state.json` - 宠物状态和位置
- `user_settings.json` - 用户设置
- `photo_cache/` - 照片缓存目录

### 自定义设置
编辑 `user_settings.json`：
```json
{
  "pet_size": 100,           // 宠物大小百分比
  "auto_sleep_minutes": 10,  // 自动睡觉时间（分钟）
  "food_effects": true,      // 食物特效开关
  "sound_effects": false,    // 音效开关
  "start_minimized": false   // 启动时最小化
}
```

## 🐛 故障排除

### 常见问题

#### 1. 程序无法启动
**症状**：双击没反应，或闪退
**解决**：
1. 以管理员身份运行
2. 安装 [VC++运行库](https://aka.ms/vs/17/release/vc_redist.x64.exe)
3. 检查Windows更新

#### 2. 照片转换失败
**症状**：提示"无法识别人脸"
**解决**：
1. 使用正面清晰的照片
2. 确保照片中有明显人脸
3. 照片大小不超过5MB

#### 3. 宠物显示异常
**症状**：宠物显示为黑色方块
**解决**：
1. 更新显卡驱动
2. 关闭硬件加速（设置中调整）
3. 重启程序

#### 4. 杀毒软件误报
**症状**：程序被隔离或删除
**解决**：
1. 在杀毒软件中添加白名单
2. 恢复被隔离的文件
3. 暂时关闭实时保护

### 日志文件
如果遇到问题，请查看日志：
```
C:\Users\<用户名>\AppData\Roaming\桌面宠物程序\logs\
```

包含：
- `app.log` - 应用程序日志
- `error.log` - 错误日志
- `debug.log` - 调试日志（需要开启调试模式）

## 🔄 更新与卸载

### 检查更新
程序启动时自动检查更新，也可手动检查：
1. 右键系统托盘图标
2. 选择"检查更新"
3. 如有新版本，提示下载

### 卸载程序
**方法一**（控制面板）：
1. 控制面板 → 程序和功能
2. 找到"桌面宠物程序"
3. 点击"卸载"

**方法二**（安装目录）：
1. 打开安装目录
2. 运行 `unins000.exe`
3. 按向导卸载

**保留用户数据**：
卸载时选择"保留我的数据"，下次安装可恢复。

## 📱 移动设备支持

### 手机照片使用
1. 将手机照片传到电脑
2. 在程序中选择该照片
3. 自动适配为桌面宠物

### 多电脑同步
1. 备份 `AppData\Roaming\桌面宠物程序\data\`
2. 复制到新电脑相同位置
3. 安装程序，宠物状态自动恢复

## 🎨 开发者信息

### 技术栈
- **语言**: Python 3.8+
- **GUI框架**: PyQt5
- **图像处理**: OpenCV, PIL
- **打包工具**: PyInstaller
- **安装程序**: Inno Setup

### 项目结构
```
desktop_pet/
├── src/main.py              # 主程序
├── config/                  # 配置文件
├── assets/                  # 资源文件
├── packaging/               # 打包脚本
└── requirements.txt         # 依赖列表
```

### 自行编译
```bash
# 1. 克隆项目
git clone https://github.com/luomodeshang/desktop-pet.git

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行开发版
python src/main.py

# 4. 打包EXE
cd packaging
python build_windows_exe.py
```

## 📞 支持与反馈

### 问题反馈
1. **GitHub Issues**: [提交问题](https://github.com/luomodeshang/desktop-pet/issues)
2. **Email**: 1024656097@qq.com
3. **文档**: 查看 [USER_GUIDE_小白版.md](USER_GUIDE_小白版.md)

### 反馈模板
```
问题描述：
操作步骤：
期望结果：
实际结果：
截图/日志：
系统信息：Windows 10/11，版本号，电脑配置
```

## 📄 许可证
MIT License - 详见 [LICENSE](LICENSE)

## 🙏 致谢
感谢所有测试用户和贡献者！

---

**开始你的桌面宠物之旅吧！** 🐾

*最后更新: 2026年4月20日 | 版本: 1.0.0 | 开发者: luomodeshang*